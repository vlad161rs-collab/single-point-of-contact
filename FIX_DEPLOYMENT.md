# Исправление проблемы с базой данных

## Проблема:
Таблица `auth_user` не существует - миграции не применены к правильной базе данных.

## Решение:

### Шаг 1: Проверьте и примените миграции

В Heroku Console выполните:

```bash
python manage.py migrate
```

Это должно создать все необходимые таблицы, включая `auth_user`.

### Шаг 2: После применения миграций создайте суперпользователя

```bash
python -c "import os, django; os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoProject.settings'); django.setup(); from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'xok1611995@yandex.ru', 'admin123') if not User.objects.filter(username='admin').exists() else print('User exists')"
```

### Альтернативный способ (если команды зависают):

1. Откройте Heroku Dashboard: https://dashboard.heroku.com/apps/single-point-of-contact
2. Перейдите в "Settings" → "Config Vars"
3. Убедитесь, что `DATABASE_URL` установлен
4. В разделе "More" → "Run console" выполните команды выше

### Если проблема сохраняется:

Проверьте подключение к базе данных:

```bash
python manage.py dbshell
```

Если подключение работает, выполните SQL напрямую для проверки таблиц:

```sql
\dt
```

Это покажет все таблицы в базе данных.

