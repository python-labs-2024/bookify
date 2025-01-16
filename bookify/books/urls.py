# books/urls.py
from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

app_name = "books"

urlpatterns = [
    path("", views.book_list, name="book_list"),
    path("book/<int:pk>/", views.book_detail, name="book_detail"),
    path("book/add/", views.add_book, name="add_book"),
    path("book/delete/<int:pk>/", views.delete_book, name="delete_book"),
    path("book/<int:pk>/add_review/", views.add_review, name="add_review"),
    path("genres/", views.genre_list, name="genre_list"),
    path("genres/add/", views.add_genre, name="add_genre"),
    path("genres/edit/<int:pk>/", views.edit_genre, name="edit_genre"),
    path("genres/delete/<int:pk>/", views.delete_genre, name="delete_genre"),
    path(
        "genres/<str:genre_name>/",
        views.genre_recommendations,
        name="genre_recommendations",
    ),
    path("register/", views.register, name="register"),
]
