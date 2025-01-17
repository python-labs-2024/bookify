import pytest
from books.models import Book, Genre, Review
from django.contrib.auth.models import User


@pytest.mark.django_db
def test_genre_str():
    genre = Genre.objects.create(name="Fantasy")
    assert str(genre) == "Fantasy"


@pytest.mark.django_db
def test_book_str():
    user = User.objects.create_user(username="testuser", password="12345")
    book = Book.objects.create(
        title="Test Book", author="Test Author", description="Desc", created_by=user
    )
    assert str(book) == "Test Book"


@pytest.mark.django_db
def test_review_str():
    user = User.objects.create_user(username="tester", password="12345")
    book = Book.objects.create(title="Test", author="Author")
    review = Review.objects.create(book=book, user=user, rating=4, text="Nice")
    assert "tester" in str(review)
    assert "Test" in str(review)


@pytest.mark.django_db
def test_book_average_rating_property(db):
    """
    Проверяем, что @property average_rating
    корректно считает средний рейтинг из Review.
    """
    user = User.objects.create_user(username="testuser", password="12345")
    book = Book.objects.create(title="Test Book", author="Test Author", created_by=user)
    Review.objects.create(book=book, user=user, rating=4)
    Review.objects.create(book=book, user=user, rating=2)

    avg = book.average_rating

    assert avg == 3.0, "Средний рейтинг должен быть (4+2)/2 = 3.0"
