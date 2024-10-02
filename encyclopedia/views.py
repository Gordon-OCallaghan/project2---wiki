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
        
def new_page(request):
    if request.method =="GET":
        return render(request, "encyclopedia/new_page.html")
    else:
        title = request.POST['title']
        content = request.POST['content']
        #error check to see if title already exists 
        duplicate = util.get_entry(title)
        if duplicate is not None:
            return render(request, "encyclopedia/error.html", {
                "error_message": "The requested page already exists."
            })
        else:
            #if entry is new we are going to save it,use save_entry function from util.py
            util.save_entry(title, content)
            converted_content = convert_markdown(title)
            return render(request, "encyclopedia/entry.html", {
                "title": title,
                "entry": converted_content
            })
        

def edit(request):
        if request.method == "POST":
            title = request.POST['entry_title']
            content = util.get_entry(title)
            return render(request, "encyclopedia/edit.html", {
                "title": title,
                "content": content
            })
        
def save_edit(request):
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']
        util.save_entry(title, content)
        converted_content = convert_markdown(title)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "entry": converted_content
        })

