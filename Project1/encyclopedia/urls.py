from django.urls import path

from . import views


app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("Random", views.random, name="random"),
    path("EditPage", views.edit_page, name="edit"),
    path("search", views.search_route, name="search"),
    path("SimilarResults", views.search_route, name="search"),
    path("NewPage", views.new_page, name="new"),
    path("<str:entry>", views.entry, name="entry")
]
