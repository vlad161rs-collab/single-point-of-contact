# Инструкция по развёртыванию на Heroku

## Подготовка к развёртыванию

### 1. Установка зависимостей

Убедитесь, что все зависимости установлены:

```bash
pip install -r requirements.txt
```

### 2. Локальная проверка с PostgreSQL (опционально)

Для тестирования с PostgreSQL локально:

1. Установите PostgreSQL
2. Создайте базу данных:
```sql
CREATE DATABASE your_db_name;
CREATE USER your_user WITH PASSWORD 'your_password';
ALTER ROLE your_user SET client_encoding TO 'utf8';
ALTER ROLE your_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE your_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE your_db_name TO your_user;
```

3. Установите переменную окружения:
```bash
# Windows PowerShell
$env:DATABASE_URL="postgresql://your_user:your_password@localhost:5432/your_db_name"

# Linux/Mac
export DATABASE_URL="postgresql://your_user:your_password@localhost:5432/your_db_name"
```

4. Примените миграции:
```bash
python manage.py migrate
```

5. Создайте суперпользователя:
```bash
python manage.py createsuperuser
```

### 3. Подготовка статических файлов

```bash
python manage.py collectstatic --noinput
```

## Развёртывание на Heroku

### 1. Установка Heroku CLI

Скачайте и установите Heroku CLI с https://devcenter.heroku.com/articles/heroku-cli

### 2. Вход в Heroku

```bash
heroku login
```

### 3. Создание приложения на Heroku

```bash
heroku create your-app-name
```

### 4. Добавление PostgreSQL аддона

```bash
heroku addons:create heroku-postgresql:mini
```

### 5. Настройка переменных окружения

```bash
# Секретный ключ Django (сгенерируйте новый!)
heroku config:set SECRET_KEY="your-secret-key-here"

# Режим отладки (False для продакшена)
heroku config:set DEBUG=False

# Email настройки
heroku config:set EMAIL_HOST_USER="xok1611995@yandex.ru"
heroku config:set EMAIL_HOST_PASSWORD="your-app-password"

# Admin email
heroku config:set ADMIN_EMAIL="xok1611995@yandex.ru"
```

**Важно:** Сгенерируйте новый SECRET_KEY для продакшена:
```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

### 6. Развёртывание кода

```bash
# Если используете Git
git init
git add .
git commit -m "Initial commit"
git push heroku main

# Или если используете master
git push heroku master
```

### 7. Применение миграций

```bash
heroku run python manage.py migrate
```

### 8. Создание суперпользователя

```bash
heroku run python manage.py createsuperuser
```

### 9. Сбор статических файлов

```bash
heroku run python manage.py collectstatic --noinput
```

### 10. Проверка приложения

```bash
heroku open
```

## Полезные команды Heroku

```bash
# Просмотр логов
heroku logs --tail

# Запуск команд в продакшене
heroku run python manage.py <command>

# Просмотр переменных окружения
heroku config

# Открыть приложение в браузере
heroku open

# Перезапуск приложения
heroku restart

# Масштабирование (если нужно)
heroku ps:scale web=1
```

## Миграция данных из SQLite в PostgreSQL

Если у вас есть данные в SQLite, которые нужно перенести:

1. Экспорт данных из SQLite:
```bash
python manage.py dumpdata > data.json
```

2. Настройте DATABASE_URL для PostgreSQL на Heroku (уже настроено через аддон)

3. Импорт данных в PostgreSQL:
```bash
heroku run python manage.py loaddata data.json
```

## Проверка работоспособности

После развёртывания проверьте:

1. ✅ Главная страница открывается
2. ✅ Статические файлы загружаются (CSS, изображения)
3. ✅ Вход в систему работает
4. ✅ Регистрация работает
5. ✅ Создание заявок работает
6. ✅ Email уведомления отправляются
7. ✅ Админ-панель доступна

## Решение проблем

### Проблема: Статические файлы не загружаются

Решение:
```bash
heroku run python manage.py collectstatic --noinput
```

### Проблема: Ошибка базы данных

Решение:
```bash
heroku run python manage.py migrate
```

### Проблема: Email не отправляется

Проверьте:
1. Переменные окружения EMAIL_HOST_USER и EMAIL_HOST_PASSWORD установлены
2. Используется пароль приложения Yandex, а не обычный пароль
3. Проверьте логи: `heroku logs --tail`

### Проблема: CSRF ошибки

Убедитесь, что:
- DEBUG=False в продакшене
- ALLOWED_HOSTS содержит домен Heroku
- CSRF_COOKIE_SECURE=True (автоматически при DEBUG=False)

## Обновление приложения

После внесения изменений:

```bash
git add .
git commit -m "Описание изменений"
git push heroku main
heroku run python manage.py migrate
heroku restart
```

## Резервное копирование базы данных

```bash
# Создание резервной копии
heroku pg:backups:capture

# Скачивание резервной копии
heroku pg:backups:download
```

## Дополнительные рекомендации

1. **Медиа файлы**: Для продакшена рекомендуется использовать облачное хранилище (AWS S3, Cloudinary)
2. **Мониторинг**: Настройте мониторинг через Heroku Metrics или внешние сервисы
3. **Логирование**: Используйте `heroku logs --tail` для отслеживания ошибок
4. **Безопасность**: Регулярно обновляйте зависимости: `pip list --outdated`

