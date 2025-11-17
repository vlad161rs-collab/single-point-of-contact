#!/usr/bin/env python
"""
Скрипт проверки готовности к развёртыванию на Heroku
"""
import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

def check_file_exists(filename, required=True):
    """Проверка существования файла"""
    filepath = BASE_DIR / filename
    exists = filepath.exists()
    status = "✓" if exists else "✗"
    print(f"{status} {filename} {'(обязательно)' if required else '(опционально)'}")
    if required and not exists:
        return False
    return True

def check_settings():
    """Проверка настроек settings.py"""
    print("\n=== Проверка settings.py ===")
    settings_file = BASE_DIR / 'djangoProject' / 'settings.py'
    
    if not settings_file.exists():
        print("✗ settings.py не найден!")
        return False
    
    with open(settings_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    checks = {
        'dj_database_url': 'dj_database_url' in content,
        'whitenoise': 'whitenoise' in content.lower(),
        'STATIC_ROOT': 'STATIC_ROOT' in content,
        'DEBUG check': "DEBUG = os.environ.get('DEBUG'" in content,
        'SECRET_KEY env': "SECRET_KEY = os.environ.get('SECRET_KEY'" in content,
    }
    
    all_ok = True
    for check_name, result in checks.items():
        status = "✓" if result else "✗"
        print(f"{status} {check_name}")
        if not result:
            all_ok = False
    
    return all_ok

def check_requirements():
    """Проверка requirements.txt"""
    print("\n=== Проверка requirements.txt ===")
    req_file = BASE_DIR / 'requirements.txt'
    
    if not req_file.exists():
        print("✗ requirements.txt не найден!")
        return False
    
    required_packages = [
        'Django',
        'djangorestframework',
        'psycopg2-binary',
        'gunicorn',
        'whitenoise',
        'dj-database-url',
    ]
    
    with open(req_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    all_ok = True
    for package in required_packages:
        found = package.lower() in content.lower()
        status = "✓" if found else "✗"
        print(f"{status} {package}")
        if not found:
            all_ok = False
    
    return all_ok

def main():
    print("=" * 50)
    print("Проверка готовности к развёртыванию на Heroku")
    print("=" * 50)
    
    all_ok = True
    
    # Проверка файлов
    print("\n=== Проверка файлов ===")
    files_to_check = [
        ('requirements.txt', True),
        ('Procfile', True),
        ('runtime.txt', True),
        ('.gitignore', True),
        ('.env.example', False),
        ('DEPLOYMENT.md', False),
    ]
    
    for filename, required in files_to_check:
        if not check_file_exists(filename, required):
            all_ok = False
    
    # Проверка настроек
    if not check_settings():
        all_ok = False
    
    # Проверка зависимостей
    if not check_requirements():
        all_ok = False
    
    # Итог
    print("\n" + "=" * 50)
    if all_ok:
        print("✓ Все проверки пройдены! Проект готов к развёртыванию.")
        return 0
    else:
        print("✗ Обнаружены проблемы. Исправьте их перед развёртыванием.")
        return 1

if __name__ == '__main__':
    sys.exit(main())

