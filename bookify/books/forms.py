# books/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Book, Genre, Review


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email"]


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ["title", "author", "description", "cover_image", "genres"]
        widgets = {
            "genres": forms.CheckboxSelectMultiple(),
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["rating", "text"]
        widgets = {
            "rating": forms.NumberInput(attrs={"min": 1, "max": 5}),
        }


class GenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = ["name"]
