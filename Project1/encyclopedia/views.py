from django.http import HttpResponse
from django.shortcuts import render
from markdown2 import Markdown
import html


from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, entry):
    markdowner = Markdown()
    if request.method == "GET":
        if util.get_entry(entry) is None:
            return render(request, "encyclopedia/notfound.html")
        else:
            return render(request, "encyclopedia/entry.html", {
            "entry": markdowner.convert(util.get_entry(entry))
            })
    elif request.method == "POST":

