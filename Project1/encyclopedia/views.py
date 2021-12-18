from django.http import HttpResponse
from django import forms
from django.shortcuts import render
from markdown2 import Markdown
from . import util
from random import randint

class CreateNewPage(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'title'}), label='title')
    content = forms.CharField(widget=forms.Textarea(attrs={'cols': 30, 'rows': 1, 'class': 'content'}), label='content')

class EditPage(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'title', 'readonly': 'True'}), label='title')
    content = forms.CharField(widget=forms.Textarea(attrs={'cols': 30, 'rows': 1, 'class': 'content'}), label='content')

def index(request):
    print(f"index entries {util.list_entries()}")
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def new_page(request):
    markdowner = Markdown()
    if request.method == "GET":
        return render(request, f"encyclopedia/NewPage.html", {
            "form": CreateNewPage()
        })
    elif request.method == "POST":
        form = CreateNewPage(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]

    if title in util.list_entries():
        return render(request, "encyclopedia/error.html", {
            "err_title": "A page with that name already exists.",
            "message": "You may edit the already existing page with any additional information you have or consider"
                       " a new page title."
        })
    else:
        util.save_entry(title, content)
        return render(request, f"encyclopedia/Qentry.html", {
            "entry": markdowner.convert(util.get_entry(title))
        })



# Process a request coming from search
def search_route(request):
    markdowner = Markdown()
    requested_value = request.POST.get("q")
    if requested_value in util.list_entries():
        return render(request, f"encyclopedia/Qentry.html", {
            "entry": markdowner.convert(util.get_entry(requested_value))
        })
    else:
        entries = []
        for entry in util.list_entries():
            if entry.find(requested_value) != -1:
                entries.append(entry)
        return render(request, f"encyclopedia/SimilarResults.html", {
            "entries": entries
        })


def entry(request, entry):
    markdowner = Markdown()
    if util.get_entry(entry) is None:
       return render(request, "encyclopedia/error.html", {
           "err_title": "Page not found",
           "message": "The page you are looking for does not exist. You are welcome to create one!"
       })
    else:
        return render(request, "encyclopedia/Qentry.html", {
            "entry": markdowner.convert(util.get_entry(entry)),
            "title": entry
    })

def edit_page(request):
    markdowner = Markdown()
    if request.method == "GET":
        title = request.GET.get("q")
        content = util.get_entry(title)
        form = EditPage(initial={'content': content, 'title': title})

        return render(request, "encyclopedia/EditPage.html", {
            "form": form,
            "title": title
        })
    elif request.method == "POST":
        form = EditPage(request.POST)
        print(f"Form errors {form.errors}")
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            print(f"Title {title}")
            util.save_entry(title, content)

            return render(request, f"encyclopedia/Qentry.html", {
                "entry": markdowner.convert(util.get_entry(title))
            })

def random(request):
    markdowner = Markdown()
    list_entries = util.list_entries()
    page_idx = randint(0, len(list_entries)-1)
    page_title = list_entries[page_idx]

    return render(request, f"encyclopedia/Qentry.html", {
        "entry": markdowner.convert(util.get_entry(page_title))
    })