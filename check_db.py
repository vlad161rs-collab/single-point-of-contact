#!/usr/bin/env python
"""Проверка подключения к базе данных"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoProject.settings')
django.setup()

from django.db import connection

print("=" * 60)
print("Проверка подключения к базе данных")
print("=" * 60)
print()

# Проверяем настройки базы данных
from django.conf import settings
db_settings = settings.DATABASES['default']

print(f"ENGINE: {db_settings['ENGINE']}")
print(f"NAME: {db_settings.get('NAME', 'N/A')}")
print(f"HOST: {db_settings.get('HOST', 'N/A')}")
print(f"PORT: {db_settings.get('PORT', 'N/A')}")
print(f"USER: {db_settings.get('USER', 'N/A')}")
print()

# Проверяем подключение
try:
    with connection.cursor() as cursor:
        cursor.execute("SELECT version();")
        version = cursor.fetchone()[0]
        print(f"✓ Подключение успешно!")
        print(f"  PostgreSQL версия: {version.split(',')[0]}")
        print()
        
        # Проверяем существующие таблицы
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """)
        tables = cursor.fetchall()
        
        if tables:
            print(f"✓ Найдено таблиц: {len(tables)}")
            print("  Таблицы:")
            for table in tables[:10]:  # Показываем первые 10
                print(f"    - {table[0]}")
            if len(tables) > 10:
                print(f"    ... и ещё {len(tables) - 10} таблиц")
        else:
            print("✗ Таблицы не найдены. Нужно применить миграции.")
            
except Exception as e:
    print(f"✗ Ошибка подключения: {e}")

