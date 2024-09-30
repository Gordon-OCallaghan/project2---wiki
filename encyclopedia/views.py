from django.shortcuts import render
from markdown2 import Markdown

from . import util

def convert_markdown(title):
    content = util.get_entry(title)
    markdowner = Markdown()
    if content is None:             #if content is None return None
        return None
    else:                           #else content is not None return converted content
        return markdowner.convert(content)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })



