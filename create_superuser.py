#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoProject.settings')
django.setup()

from django.contrib.auth.models import User

# Создаём суперпользователя
username = 'admin'
email = 'xok1611995@yandex.ru'
password = 'admin123'

if User.objects.filter(username=username).exists():
    print(f'User {username} already exists')
    user = User.objects.get(username=username)
    user.set_password(password)
    user.is_superuser = True
    user.is_staff = True
    user.save()
    print(f'Updated user {username}')
else:
    User.objects.create_superuser(username, email, password)
    print(f'Created superuser {username}')

