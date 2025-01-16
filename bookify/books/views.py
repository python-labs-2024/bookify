from django.shortcuts import get_object_or_404, redirect, render

from .forms import BookForm, ReviewForm
from .models import Book, Genre, Review


def book_list(request):
    """Главная страница со списком всех книг."""
    books = Book.objects.all()
    return render(request, "books/book_list.html", {"books": books})


def book_detail(request, pk):
    """Детальная страница книги."""
    book = get_object_or_404(Book, pk=pk)
    reviews = book.reviews.all()
    review_form = ReviewForm()
    return render(
        request,
        "books/book_detail.html",
        {"book": book, "reviews": reviews, "review_form": review_form},
    )


def add_book(request):
    """Добавление новой книги."""
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("books:book_list")
    else:
        form = BookForm()
    return render(request, "books/add_book.html", {"form": form})


def delete_book(request, pk):
    """Удаление книги."""
    book = get_object_or_404(Book, pk=pk)
    book.delete()
    return redirect("books:book_list")


def add_review(request, pk):
    """Добавление отзыва к книге."""
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.book = book
            review.save()
    return redirect("books:book_detail", pk=pk)


def genre_recommendations(request, genre_name):
    """Рекомендации книг по заданному жанру."""
    genre = get_object_or_404(Genre, name=genre_name)
    # Выберем все книги, которые относятся к данному жанру
    books = genre.books.all()
    return render(
        request, "books/genre_recommendations.html", {"genre": genre, "books": books}
    )
