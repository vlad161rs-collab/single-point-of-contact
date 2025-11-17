# Быстрый старт для развёртывания на Heroku

## Шаг 1: Подготовка

```bash
# Установите зависимости
pip install -r requirements.txt

# Проверьте готовность
python pre_deploy_check.py
```

## Шаг 2: Локальное тестирование (опционально)

```bash
# Примените миграции
python manage.py migrate

# Создайте суперпользователя
python manage.py createsuperuser

# Соберите статические файлы
python manage.py collectstatic --noinput

# Запустите сервер
python manage.py runserver
```

## Шаг 3: Развёртывание на Heroku

```bash
# 1. Войдите в Heroku
heroku login

# 2. Создайте приложение
heroku create your-app-name

# 3. Добавьте PostgreSQL
heroku addons:create heroku-postgresql:mini

# 4. Установите переменные окружения
heroku config:set SECRET_KEY="$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')"
heroku config:set DEBUG=False
heroku config:set EMAIL_HOST_USER="xok1611995@yandex.ru"
heroku config:set EMAIL_HOST_PASSWORD="your-app-password"
heroku config:set ADMIN_EMAIL="xok1611995@yandex.ru"

# 5. Разверните код
git init
git add .
git commit -m "Initial deployment"
git push heroku main

# 6. Примените миграции
heroku run python manage.py migrate

# 7. Создайте суперпользователя
heroku run python manage.py createsuperuser

# 8. Соберите статические файлы
heroku run python manage.py collectstatic --noinput

# 9. Откройте приложение
heroku open
```

## Важные замечания

1. **SECRET_KEY**: Обязательно сгенерируйте новый ключ для продакшена!
2. **EMAIL_HOST_PASSWORD**: Используйте пароль приложения Yandex, а не обычный пароль
3. **DEBUG**: Всегда устанавливайте `False` в продакшене
4. **База данных**: Heroku автоматически создаст DATABASE_URL при добавлении PostgreSQL аддона

## Проверка после развёртывания

```bash
# Просмотр логов
heroku logs --tail

# Проверка переменных окружения
heroku config

# Запуск команд Django
heroku run python manage.py <command>
```

## Миграция данных (если нужно)

Если у вас есть данные в SQLite:

```bash
# 1. Экспорт
python manage.py dumpdata > data.json

# 2. Импорт на Heroku
heroku run python manage.py loaddata data.json
```

## Дополнительная информация

- Полная инструкция: [DEPLOYMENT.md](DEPLOYMENT.md)
- Чеклист проверки: [CHECKLIST.md](CHECKLIST.md)

