from django.contrib.auth.models import User
from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    description = models.TextField()
    genres = models.ManyToManyField(Genre, related_name="books")
    cover_image = models.URLField(blank=True, null=True)  # Можно хранить URL обложки

    def __str__(self):
        return self.title


class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="reviews")
    # Если планируется использовать Django-аутентификацию, можно связать с User
    user_name = models.CharField(max_length=100)
    rating = models.PositiveIntegerField(default=1)  # от 1 до 5, например
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Отзыв от {self.user_name} на книгу «{self.book}»"
