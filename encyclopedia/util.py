import re

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


def list_entries():

    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))


def save_entry(title, content):
    
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))


def get_entry(title):

    try:
        f = default_storage.open(f"entries/{title}.md")
        return f.read().decode("utf-8")
    except FileNotFoundError:
        return None
        
def related_titles(title):
    
    related = []

    for entry_name in list_entries():
            if title.lower() in entry_name.lower() or entry_name.lower() in title.lower():
                related.append(entry_name)

    return related
