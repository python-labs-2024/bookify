from django.contrib import admin

from .models import Book, Genre, Review


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "author")
    search_fields = ("title", "author")
    list_filter = ("genres",)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("id", "book", "user_name", "rating", "created_at")
    list_filter = ("book", "rating")
