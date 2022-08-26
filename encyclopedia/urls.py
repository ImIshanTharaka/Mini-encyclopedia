from importlib.metadata import entry_points
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),            #if the path is this then index function in views.py is called
    path("search", views.search, name="search"),
    path("newpage", views.newpage, name="newpage"),
    path("random", views.randompage, name="randompage"),   
    path("wiki/<str:title>", views.entry, name="entry"),    # <str:title> expect to receive a str as a variable
    path("wiki/<str:title>/edit", views.edit, name="edit"),     
]
