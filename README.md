# 📚 Bookify

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)


Курсовая работа по дисциплине "Разработка приложений на Python". 

## Task
Название проекта: **bookify**

Приложение для рекомендации и рейтинг книг по жанрам.
1. приложение (**django**), добавление и удаление книг
2. рейтинг и отзывов книг
3. рекомендации по жанрам

## Demo

🚀🚀🚀 Приложение развёрнуто на [bookify.tishenko.dev](https://bookify.tishenko.dev/) 🚀🚀🚀

## Local Setup Guide

Склонировать репозиторий

```bash
git clone https://github.com/python-labs-2024/bookify.git
cd bookify
```

Создать виртуальное окружение

```bash
virtualenv venv
```

И активировать его
```powershell
# Для Windows
venv\Scripts\activate
```

```bash
# Для Linux
source venv/bin/activate
```

Установить зависимости

```bash
pip install -r requirements.txt
```

Создать миграции и создать суперпользователя

```bash
cd bookify

python manage.py makemigrations books
python manage.py migrate

python manage.py createsuperuser
```

Запустить сервер Django
```bash
python manage.py runserver
```

🎉 Готово! Приложение развёрнуто на http://127.0.0.1:8000/.