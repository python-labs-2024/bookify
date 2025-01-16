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

> **Примечание:** Проект работает на **Django 5**, поэтому нужен как минимум Python **3.10**.


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


## Deployment with Gunicorn and Nginx

### Подготовка

```bash
# Далее в инструкции предполагается, что мы в домашней директории пользователя
git clone https://github.com/python-labs-2024/bookify.git
cd bookify

# Возможно на сервере другая версия Python и команду придётся поменять, но 3.10 это минимум
python3.10 -m venv venv 
source venv/bin/activate

pip install -r requirements.txt
pip install gunicorn

cd bookify
python manage.py makemigrations books
python manage.py migrate

python manage.py createsuperuser

# Можно перейти по адресу сервера в браузере на порт 8000 и убедиться,
# что всё работает (ну почти, стилей тут не будет)
# Не на всех VDS может быть открыт 8000 порт, в таком случае просто 
# смотрим на отсутствие ошибок
gunicorn --bind 0.0.0.0:8000 archers.wsgi
```

### Добавляем конфигурацию Gunicorn в systemd 

Настроиваем сокет для `systemd`, чтобы приложение работало в фоне и автоматически запускалось системой

```bash
sudo nano /etc/systemd/system/bookify.socket
```

```
[Unit]
Description=bookify socket

[Socket]
ListenStream=/run/bookify.sock

[Install]
WantedBy=sockets.target
```

Теперь настроим сервис `systemd`
```bash
sudo nano /etc/systemd/system/bookify.service
```

> **Примечание:** Не забудьте заменить пользователя airty на вашего, а ещё лучше вообще создать отдельного.
```
[Unit]
Description=bookify gunicorn daemon
Requires=bookify.socket
After=network.target

[Service]
User=arity
Group=arity
WorkingDirectory=/home/arity/bookify/bookify
ExecStart=/home/arity/bookify/venv/bin/gunicorn \
          --access-logfile - \
          --workers 1 \
          --bind unix:/run/bookify.sock \
          bookify.wsgi:application

[Install]
WantedBy=multi-user.target
```

Теперь активируем сокет и добавим в автозапуск
```bash
sudo systemctl start bookify.socket
sudo systemctl enable bookify.socket
```

### Настраиваем Nginx

Собираем статику (стили, скрипты, картинки) и переносим в `/var/www/` - именно этот каталог обычно используются для её хранения, к тому же иначе будут проблемы с доступами, NGINX просто не сможет работать с нашими файлами.

```bash
# Команда собирает всю статику Django в папку, которая
# указана в settings.py (см. STATIC_ROOT)
python manage.py collectstatic

# Переносим статику из staticfiles (см. STATIC_ROOT) в /var/www/
sudo mkdir /var/www/bookify
sudo cp -r staticfiles /var/www/bookify/static
```

Теперь можно настроить NGINX
```bash
sudo nano /etc/nginx/sites-available/default
```
В файле указываем следующий конфиг
```nginx
server {
    listen 80;
    server_name your_domain_or_ip;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /var/www/bookify;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/bookify.sock;
    }
}
```

Добавляем конфиг в активные конфиги
```bash
sudo ln -s /etc/nginx/sites-available/bookify /etc/nginx/sites-enabled
```

Перезапускаем Nginx, чтобы изменения вступили в силу
```bash
sudo systemctl restart nginx
```

### Если что-то идёт не так...

Логи NGINX
```bash
# Информация обо всех запросах
sudo tail -f /var/log/nginx/access.log
# Информация обо всех ошибках и предупреждениях
sudo tail -f /var/log/nginx/error.log
# Проверка корректности конфигов
sudo nginx -t
# Очистка логов без необходимости перезапуска NGINX
sudo truncate -s 0 /var/log/nginx/access.log
sudo truncate -s 0 /var/log/nginx/error.log
```

Логи Gunicorn
```bash
# -f - показывает последние логи
sudo journalctl -u bookify -f
sudo journalctl -u bookify.socket -f
```

