from django import forms

from .models import Book, Genre, Review


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
        fields = ["user_name", "rating", "text"]
        widgets = {
            "rating": forms.NumberInput(attrs={"min": 1, "max": 5}),
        }


class GenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = ["name"]
