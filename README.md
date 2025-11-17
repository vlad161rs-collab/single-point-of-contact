# Django Knowledge Base System

Система управления базой знаний с порталом самообслуживания для обработки заявок пользователей.

## Основные возможности

- 📚 База знаний со статьями
- 📝 Система заявок с категоризацией
- 💬 Комментарии к статьям и заявкам
- 👥 Управление пользователями и ролями
- 📧 Email уведомления
- 🔐 Система регистрации и одобрения пользователей

## Технологии

- Django 5.1.3
- Django REST Framework
- PostgreSQL (продакшен) / SQLite (разработка)
- Pillow для работы с изображениями
- WhiteNoise для статических файлов

## Быстрый старт

### Локальная разработка

1. Клонируйте репозиторий
2. Создайте виртуальное окружение:
```bash
python -m venv env
env\Scripts\activate  # Windows
source env/bin/activate  # Linux/Mac
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Настройте переменные окружения (создайте `.env` на основе `.env.example`)

5. Примените миграции:
```bash
python manage.py migrate
```

6. Создайте суперпользователя:
```bash
python manage.py createsuperuser
```

7. Запустите сервер:
```bash
python manage.py runserver
```

### Развёртывание на Heroku

См. подробную инструкцию в [DEPLOYMENT.md](DEPLOYMENT.md)

## Структура проекта

```
djangoProject/
├── djangoProject/          # Основные настройки проекта
│   ├── settings.py        # Настройки Django
│   ├── urls.py            # Главный URL конфиг
│   └── wsgi.py            # WSGI конфигурация
├── knowledgebase/         # Приложение базы знаний
│   ├── models.py          # Модели (Article, Request, Comment)
│   ├── views.py           # Представления
│   ├── forms.py           # Формы
│   └── signals.py        # Сигналы для уведомлений
├── portal/                # Портал самообслуживания
│   ├── models.py          # Модели (UserProfile, Department)
│   ├── views.py           # Представления
│   └── forms.py           # Формы регистрации
├── static/                # Статические файлы
├── media/                 # Медиа файлы
├── requirements.txt       # Зависимости Python
├── Procfile               # Конфигурация Heroku
└── runtime.txt            # Версия Python
```

## Модели данных

### Knowledge Base
- **Article** - статьи базы знаний
- **Request** - заявки пользователей
- **Comment** - комментарии к статьям и заявкам

### Portal
- **UserProfile** - профили пользователей
- **Department** - отделы организации
- **UserRegistrationRequest** - заявки на регистрацию

## API

REST API доступен по адресу `/knowledgebase/api/requests/`

- GET - список всех заявок
- POST - создание новой заявки (требует аутентификации)

## Переменные окружения

См. `.env.example` для списка необходимых переменных окружения.

## Лицензия

Проект создан в рамках производственной практики.

## Автор

Разработано для системы управления базой знаний организации.

