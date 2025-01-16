from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import PermissionDenied
from django.db.models import Avg
from django.shortcuts import get_object_or_404, redirect, render

from .forms import BookForm, CustomUserCreationForm, GenreForm, ReviewForm
from .models import Book, Genre, Review


def register(request):
    """Регистрация нового пользователя."""
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # сразу авторизуем после регистрации
            return redirect("books:book_list")
    else:
        form = CustomUserCreationForm()
    return render(request, "accounts/register.html", {"form": form})


def logout(requst):
    return render(requst, "accounts/logout.html")


@login_required
def my_books(request):
    """Список книг, добавленных текущим пользователем."""
    books = Book.objects.filter(created_by=request.user)
    return render(request, "books/my_books.html", {"books": books})


def books_rating(request):
    """
    Страница со всеми книгами, отсортированными по убыванию среднего рейтинга.
    """
    # Переименуем аннотацию в avg_rating
    books = Book.objects.annotate(avg_rating=Avg("reviews__rating")).order_by(
        "-avg_rating"
    )
    return render(request, "books/books_rating.html", {"books": books})


def book_list(request):
    """Главная страница со списком всех книг."""
    books = Book.objects.all()
    return render(request, "books/book_list.html", {"books": books})


def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    reviews = book.reviews.all()
    review_form = ReviewForm()

    user_has_review = False
    if request.user.is_authenticated:
        user_has_review = reviews.filter(user=request.user).exists()

    return render(
        request,
        "books/book_detail.html",
        {
            "book": book,
            "reviews": reviews,
            "review_form": review_form,
            "user_has_review": user_has_review,
        },
    )


@login_required
def edit_book(request, pk):
    """Редактирование книги, только для её создателя."""
    book = get_object_or_404(Book, pk=pk)
    # Проверяем, что текущий пользователь – владелец:
    if book.created_by != request.user:
        raise PermissionDenied("Вы не можете редактировать чужую книгу.")

    if request.method == "POST":
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect("books:book_detail", pk=book.pk)
    else:
        form = BookForm(instance=book)

    return render(request, "books/edit_book.html", {"form": form, "book": book})


@login_required
def add_book(request):
    """Добавление новой книги (только авторизованный пользователь)."""
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save(commit=False)
            book.created_by = request.user
            book.save()
            form.save_m2m()  # сохраняем многие-ко-многим
            return redirect("books:book_list")
    else:
        form = BookForm()
    return render(request, "books/add_book.html", {"form": form})


@login_required
def delete_book(request, pk):
    """Удаление книги (только если user == created_by)."""
    book = get_object_or_404(Book, pk=pk)
    if book.created_by != request.user:
        # Если не совпадает, то выбрасываем ошибку 403
        raise PermissionDenied("Вы не можете удалять чужие книги.")

    book.delete()
    return redirect("books:book_list")


@login_required
def add_review(request, pk):
    book = get_object_or_404(Book, pk=pk)

    # Проверяем, не оставил ли уже этот пользователь отзыв
    existing_review = Review.objects.filter(book=book, user=request.user).first()
    if existing_review:
        # Если уже есть отзыв, можно показать сообщение или
        # перенаправить на страницу книги с сообщением
        # Для простоты сделаем редирект с GET-параметром
        return redirect("books:book_detail", pk=pk)

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.book = book
            review.user = request.user
            review.save()
    return redirect("books:book_detail", pk=pk)


@login_required
def edit_review(request, pk):
    """Редактирование отзыва, только если пользователь – автор."""
    review = get_object_or_404(Review, pk=pk)
    # Проверяем владельца
    if review.user != request.user:
        raise PermissionDenied("Нельзя редактировать чужой отзыв.")

    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect("books:book_detail", pk=review.book.pk)
    else:
        form = ReviewForm(instance=review)

    return render(request, "books/edit_review.html", {"form": form, "review": review})


def genre_recommendations(request, genre_name):
    """Рекомендации книг по заданному жанру."""
    genre = get_object_or_404(Genre, name=genre_name)
    # Выберем все книги, которые относятся к данному жанру
    books = genre.books.all()
    return render(
        request, "books/genre_recommendations.html", {"genre": genre, "books": books}
    )


def genre_list(request):
    """Страница со всеми жанрами."""
    genres = Genre.objects.all()
    return render(request, "books/genre_list.html", {"genres": genres})


@login_required
def add_genre(request):
    """Добавить новый жанр."""
    if request.method == "POST":
        form = GenreForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("books:genre_list")
    else:
        form = GenreForm()
    return render(request, "books/add_genre.html", {"form": form})


@login_required
def edit_genre(request, pk):
    """Редактировать жанр."""
    genre = get_object_or_404(Genre, pk=pk)
    if request.method == "POST":
        form = GenreForm(request.POST, instance=genre)
        if form.is_valid():
            form.save()
            return redirect("books:genre_list")
    else:
        form = GenreForm(instance=genre)
    return render(request, "books/edit_genre.html", {"form": form})


@login_required
def delete_genre(request, pk):
    """Удалить жанр."""
    genre = get_object_or_404(Genre, pk=pk)
    genre.delete()
    return redirect("books:genre_list")
