from importlib.resources import contents
from re import S
from this import s
from turtle import width
from django.shortcuts import render

from . import util

from markdown2 import Markdown

from django import forms  

import random 

list_entries = util.list_entries()

'''
home page
'''
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": list_entries
    })


'''
entry page
'''
def entry(request, title):
    entry_page = util.get_entry(title)      #importing function from util.py
    if entry_page is None:
        return render (request, "encyclopedia/not_found.html")
    else:
        return render (request, "encyclopedia/entry.html",{
            "entry_title": title,
            "entry": Markdown().convert(entry_page)
        })


'''
search content
'''
def search(request):
    if request.method == "POST":        #if there is a search
        query = request.POST["q"]       #getting the searched value to a parameter      
        entries = list_entries
        if util.get_entry(query) is not None:
            return render (request, "encyclopedia/entry.html",{
                "entry_title": query,
                "entry": Markdown().convert(util.get_entry(query))
            })
        elif any(str(query).lower() in s.lower() for s in entries):     #check query.lower() is a substring of a item.lower() in entries list
            matching = [s for s in entries if str(query).lower() in s.lower()]      #get the items which are query.lower() is a substring
            return render (request, "encyclopedia/search.html",{
                "matching": matching
            })
        else:
            return render (request, "encyclopedia/not_found.html")


'''
add new content
'''
class new_entry_form(forms.Form):               #class for django form in newpage.html
    title = forms.CharField(widget=forms.TextInput(attrs={'style': 'width: 400px;', 'class': 'form-control'}), label="Title")
    content = forms.CharField(widget=forms.Textarea(attrs={'style': 'height: 300px', 'class': 'form-control'}), label="Content")

def newpage(request):
    if request.method == "POST":            #if add new entry 
        form = new_entry_form(request.POST)
        if form.is_valid():
            title, content = str(form.cleaned_data["title"]).capitalize(), form.cleaned_data["content"]
            if title.lower() in (string.lower() for string in list_entries):           #if the title is already exist
                return render (request, "encyclopedia/newpage.html",{       #form back to the user with an error massage with input form data
                "massage":"Content already exist with this title.Choose different title.",
                "form":form})
            else: 
                list_entries.append(title)
                util.save_entry(title, content)     #save new entry
                return render (request, "encyclopedia/entry.html",{
                    "entry_title": title,
                    "entry": Markdown().convert(util.get_entry(title))
                })          
        else:
            return render (request, "encyclopedia/newpage.html",{       #form back to the user with input form data
                "form":form})
    return render (request, "encyclopedia/newpage.html",{       #before adding a new entry
        "form":new_entry_form()                              #returns empty form
    })


'''
edit existing content
'''
class edit_form(forms.Form):               #class for django form in edit.html
    new_content = forms.CharField(widget=forms.Textarea(attrs={'style': 'height: 300px', 'class': 'form-control'}), label="Content")

def edit(request,title):
    existing_content = util.get_entry(title)
    if existing_content is None:
        return render (request, "encyclopedia/not_found.html")
    else:
        if request.method == "POST":        #if save the edit
            form = edit_form(request.POST)
            if form.is_valid():
                new_content = form.cleaned_data["new_content"]
                util.save_entry(title, new_content)     #save new entry
                return render (request, "encyclopedia/entry.html",{
                    "entry_title": title,
                    "entry": Markdown().convert(util.get_entry(title))
                })          
            else:
                return render (request, "encyclopedia/edit.html",{       #form back to the user with input form data
                    "entry_title": title,
                    "form":form})
        return render (request, "encyclopedia/edit.html",{      #before saving
            "entry_title": title,
            "form":edit_form(initial={'new_content': existing_content})}) 

def randompage(request):
    random_entry = random.choice(list_entries)
    return render (request, "encyclopedia/randompage.html",{
            "entry_title": random_entry,
            "entry": Markdown().convert(util.get_entry(random_entry))
        })