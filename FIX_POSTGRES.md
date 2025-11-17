# Исправление проблемы с PostgreSQL

## Проблема:
Миграции применены, но таблицы не созданы в PostgreSQL.

## Решение:

### В Heroku Console выполните:

1. **Проверьте подключение к базе данных:**
```bash
python manage.py dbshell
```

Если подключение работает, вы увидите приглашение PostgreSQL. Введите `\dt` чтобы увидеть таблицы, затем `\q` для выхода.

2. **Примените миграции заново:**
```bash
python manage.py migrate --run-syncdb
```

Или просто:
```bash
python manage.py migrate
```

3. **Проверьте, что таблицы созданы:**
```bash
python manage.py dbshell
```

Затем в PostgreSQL:
```sql
\dt
```

Должны быть видны таблицы: `auth_user`, `knowledgebase_article`, `portal_userprofile` и т.д.

4. **Создайте суперпользователя:**
```bash
python -c "import os, django; os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoProject.settings'); django.setup(); from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'xok1611995@yandex.ru', 'admin123') if not User.objects.filter(username='admin').exists() else print('User exists')"
```

### Альтернатива: Проверка через Python скрипт

Выполните в Heroku Console:
```bash
python check_db.py
```

Это покажет, какая база данных используется и какие таблицы существуют.

