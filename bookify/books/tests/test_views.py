import pytest
from books.models import Book, Genre, Review
from django.contrib.auth.models import User
from django.urls import reverse


@pytest.mark.django_db
def test_book_list_view(client):
    """
    Проверяем, что список книг открывается без авторизации,
    и что в контексте передаются нужные данные.
    """
    url = reverse("books:book_list")  # смотрим, как в urls.py названо
    response = client.get(url)
    assert response.status_code == 200
    assert "Список книг" in response.content.decode()  # по заголовку проверяем


@pytest.mark.django_db
def test_add_book_requires_login(client):
    """
    Неавторизованный пользователь не может зайти на страницу добавления книги.
    Предположим, он редиректится на /login/?next=...
    """
    url = reverse("books:add_book")
    response = client.get(url)
    assert response.status_code == 302  # или 302 редирект
    assert response.url.startswith("/login/")


@pytest.mark.django_db
def test_add_book_success(client):
    user = User.objects.create_user(username="testuser", password="12345")
    client.login(username="testuser", password="12345")

    # Создаём жанр:
    fantasy = Genre.objects.create(name="Fantasy")

    url = reverse("books:add_book")
    data = {
        "title": "My Book",
        "author": "Me",
        "description": "Just a test",
        # так как genres - это M2M, Django-форма ожидает список идентификаторов:
        "genres": [fantasy.pk],
    }
    response = client.post(url, data)
    assert response.status_code == 302
    assert Book.objects.count() == 1
    new_book = Book.objects.first()
    assert new_book.title == "My Book"
    assert new_book.created_by == user
    # проверим жанры
    assert new_book.genres.count() == 1
    assert new_book.genres.first() == fantasy


@pytest.mark.django_db
def test_only_creator_can_delete_book(client):
    """
    Проверяем, что только тот, кто создал книгу, может её удалить.
    """
    user1 = User.objects.create_user(username="user1", password="pass")
    user2 = User.objects.create_user(username="user2", password="pass")
    book = Book.objects.create(title="Shared Book", author="Author", created_by=user1)

    # Попробуем удалить от имени user2
    client.login(username="user2", password="pass")
    delete_url = reverse("books:delete_book", args=[book.pk])
    response = client.get(delete_url)
    assert response.status_code == 403  # PermissionDenied -> 403

    # Убедимся, что книга не удалена
    assert Book.objects.filter(pk=book.pk).exists()

    # Теперь логинимся user1 (создатель)
    client.login(username="user1", password="pass")
    response = client.get(delete_url)

    assert response.status_code == 302
    assert not Book.objects.filter(pk=book.pk).exists()


@pytest.mark.django_db
def test_only_one_review_per_user(client):
    """
    Проверяем, что пользователь не может добавить второй отзыв к той же книге.
    """
    user = User.objects.create_user(username="reviewer", password="12345")
    book = Book.objects.create(title="Test", author="Tester")

    client.login(username="reviewer", password="12345")
    add_review_url = reverse("books:add_review", args=[book.pk])

    # Первый отзыв
    resp1 = client.post(add_review_url, {"rating": 5, "text": "Great!"})
    assert resp1.status_code == 302
    assert Review.objects.count() == 1

    # Второй отзыв (должен быть запрещён)
    resp2 = client.post(add_review_url, {"rating": 4, "text": "Another review"})
    # проверим, что кол-во отзывов не увеличилось
    assert Review.objects.count() == 1


@pytest.mark.django_db
def test_edit_review(client):
    """
    Проверяем, что автор отзыва может его отредактировать
    и изменить текст, а чужой пользователь - нет.
    """
    user1 = User.objects.create_user(username="u1", password="pass")
    user2 = User.objects.create_user(username="u2", password="pass")
    book = Book.objects.create(title="Book", author="Author")
    review = Review.objects.create(book=book, user=user1, rating=3, text="Ok")

    edit_url = reverse("books:edit_review", args=[review.pk])

    # user2 пытается редактировать
    client.login(username="u2", password="pass")
    resp = client.get(edit_url)
    assert resp.status_code == 403  # PermissionDenied

    # user1 (автор) может редактировать
    client.login(username="u1", password="pass")
    resp = client.post(edit_url, {"rating": 5, "text": "Better now"})
    assert resp.status_code == 302
    review.refresh_from_db()
    assert review.rating == 5
    assert review.text == "Better now"
