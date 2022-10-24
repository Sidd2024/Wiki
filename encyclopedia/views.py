import random
from django import forms
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from markdown import Markdown
from . import util

class SearchForm(forms.Form):

    title = forms.CharField(label='', widget=forms.TextInput(attrs={
      "class": "search",
      "placeholder": "Search Encyclopedia"}))

class CreateForm(forms.Form):
    
    title = forms.CharField(label='', widget=forms.TextInput(attrs={
      "placeholder": "Page Title"}))
    text = forms.CharField(label='', widget=forms.Textarea(attrs={
      "placeholder": "Enter Page Content using Github Markdown"
    }))

class EditForm(forms.Form):
  
  text = forms.CharField(label='', widget=forms.Textarea(attrs={
      "placeholder": "Enter Page Content using Github Markdown"
    }))


def index(request):

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "search_form": SearchForm(),
    })

def entry(request, title):

    entry = util.get_entry(title)

    if entry != None:
        
        entry_html = Markdown().convert(entry)
        return render(request, "encyclopedia/entry.html", {
          "title": title,
          "entry": entry_html,
          "search_form": SearchForm(),
          })
    else:
        
        related = util.related_titles(title)

        return render(request, "encyclopedia/notfound.html", {
          "title": title,
          "related_titles": related,
          "search_form": SearchForm(),
          })

def search(request):

    if request.method == "POST":
        form = SearchForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data["title"]
            entry = util.get_entry(title)

            print('search request: ', title)

            if entry:
                
                return redirect(reverse('entry', args=[title]))
            else:
                
                related = util.related_titles(title)

                return render(request, "encyclopedia/results.html", {
                "title": title,
                "related_titles": related,
                "search_form": SearchForm()
                })

    
    return redirect(reverse('index'))

def create(request):
    

    if request.method == "GET":
        return render(request, "encyclopedia/create.html", {
          "create_form": CreateForm(),
          "search_form": SearchForm()
        })

    elif request.method == "POST":
        form = CreateForm(request.POST)

        if form.is_valid():
          title = form.cleaned_data['title']
          text = form.cleaned_data['text']
        else:
          messages.error(request, 'Entry form not valid, please try again!')
          return render(request, "encyclopedia/create.html", {
            "create_form": form,
            "search_form": SearchForm()
          })

        if util.get_entry(title):
            messages.error(request, 'This page title already exists! Please go to that title page and edit it instead!')
            return render(request, "encyclopedia/create.html", {
              "create_form": form,
              "search_form": SearchForm()
            })
        
        else:
            util.save_entry(title, text)
            messages.success(request, f'New page "{title}" created successfully!')
            return redirect(reverse('entry', args=[title]))

def edit(request, title):

    
    if request.method == "GET":
        text = util.get_entry(title)
        
        if text == None:
            messages.error(request, f'"{title}"" page does not exist and can\'t be edited, please create a new page instead!')


        return render(request, "encyclopedia/edit.html", {
          "title": title,
          "edit_form": EditForm(initial={'text':text}),
          "search_form": SearchForm()
        })

    elif request.method == "POST":
        form = EditForm(request.POST)

        if form.is_valid():
          text = form.cleaned_data['text']
          util.save_entry(title, text)
          messages.success(request, f'Entry "{title}" updated successfully!')
          return redirect(reverse('entry', args=[title]))

        else:
          messages.error(request, f'Editing form not valid, please try again!')
          return render(request, "encyclopedia/edit.html", {
            "title": title,
            "edit_form": form,
            "search_form": SearchForm()
          })

def random_title(request):

    titles = util.list_entries()
    title = random.choice(titles)

    return redirect(reverse('entry', args=[title]))
