from django.contrib.auth import login, logout
from django.shortcuts import get_object_or_404, redirect, render


def custom_logout(request):
    """Разлогиниться и перейти на главную."""
    logout(request)
    return redirect("books:book_list")
