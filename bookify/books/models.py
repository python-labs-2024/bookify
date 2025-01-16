from django.contrib.auth.models import User
from django.db import models
from django.db.models import Avg  # для подсчёта среднего рейтинга


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    description = models.TextField()
    genres = models.ManyToManyField(Genre, related_name="books")
    cover_image = models.URLField(blank=True, null=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="created_books",
    )  # пользователь, создавший книгу

    def __str__(self):
        return self.title

    @property
    def average_rating(self):
        """Среднее значение рейтинга по всем отзывам"""
        avg_rating = self.reviews.aggregate(Avg("rating"))["rating__avg"]
        if avg_rating is not None:
            return round(avg_rating, 1)  # округлим до 1 знака после запятой
        return 0


class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    rating = models.PositiveIntegerField(default=1)  # от 1 до 5
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Отзыв от {self.user.username} на «{self.book}»"
