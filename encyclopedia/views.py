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


def entry(request, title):
    #Error checking first 
    #Does the file exist 
    entry_content = convert_markdown(title)
    if entry_content is None:
        return render(request, "encyclopedia/error.html", {
            "error_message": "The requested page was not found."
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "entry": entry_content
        })
    
def search(request):
    if request.method == "POST":
        search_query = request.POST['q']
        content = convert_markdown(search_query)
        if content is not None:
            return render (request, "encyclopedia/entry.html", {
                "title" : search_query,
                "entry" : content
            })
        else: #This is for partial search results 
            allEntries = util.list_entries()
            results = [] #List to store partial search results
            for entry in allEntries:
                if search_query.lower() in entry.lower():
                    results.append(entry)
            return render(request, "encyclopedia/search.html", {
                "results" : results
            })