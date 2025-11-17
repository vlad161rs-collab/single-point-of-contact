# Пошаговое развёртывание на Heroku

## Быстрый способ (автоматический)

Запустите скрипт:
```powershell
powershell -ExecutionPolicy Bypass -File deploy_to_heroku.ps1
```

## Ручной способ (пошагово)

### Шаг 1: Настройка Git

```powershell
git config user.email "ваш@email.com"
git config user.name "Ваше Имя"
```

### Шаг 2: Добавление файлов и коммит

```powershell
git add .
git commit -m "Initial commit: Django Knowledge Base System"
```

### Шаг 3: Вход в Heroku

```powershell
heroku login
```

Откроется браузер для входа. Войдите в свой аккаунт Heroku.

### Шаг 4: Создание приложения

```powershell
heroku create your-app-name
```

Или без имени (Heroku сгенерирует автоматически):
```powershell
heroku create
```

### Шаг 5: Добавление PostgreSQL

```powershell
heroku addons:create heroku-postgresql:mini
```

### Шаг 6: Настройка переменных окружения

```powershell
# Генерация SECRET_KEY
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Установка переменных (замените YOUR_SECRET_KEY на сгенерированный ключ)
heroku config:set SECRET_KEY="YOUR_SECRET_KEY"
heroku config:set DEBUG=False
heroku config:set EMAIL_HOST_USER="xok1611995@yandex.ru"
heroku config:set EMAIL_HOST_PASSWORD="ваш_пароль_приложения"
heroku config:set ADMIN_EMAIL="xok1611995@yandex.ru"
```

**Важно:** Heroku автоматически установит `DATABASE_URL` при добавлении PostgreSQL аддона.

### Шаг 7: Развёртывание кода

```powershell
git push heroku master
```

Или если используете `main`:
```powershell
git push heroku main
```

### Шаг 8: Применение миграций

```powershell
heroku run python manage.py migrate
```

### Шаг 9: Сбор статических файлов

```powershell
heroku run python manage.py collectstatic --noinput
```

### Шаг 10: Создание суперпользователя

```powershell
heroku run python manage.py createsuperuser
```

Следуйте инструкциям на экране.

### Шаг 11: Открытие приложения

```powershell
heroku open
```

## Проверка работы

После развёртывания проверьте:

1. ✅ Главная страница открывается
2. ✅ Статические файлы загружаются
3. ✅ Админ-панель доступна
4. ✅ Регистрация работает
5. ✅ Email уведомления отправляются

## Полезные команды

```powershell
# Просмотр логов
heroku logs --tail

# Просмотр переменных окружения
heroku config

# Выполнение команд Django
heroku run python manage.py <command>

# Перезапуск приложения
heroku restart

# Масштабирование
heroku ps:scale web=1

# Просмотр информации о приложении
heroku info
```

## Решение проблем

### Проблема: Ошибка при push

**Решение:** Убедитесь, что вы в нужной ветке:
```powershell
git branch
git checkout master  # или main
```

### Проблема: Статические файлы не загружаются

**Решение:**
```powershell
heroku run python manage.py collectstatic --noinput
```

### Проблема: Ошибка базы данных

**Решение:**
```powershell
heroku run python manage.py migrate
```

### Проблема: Email не отправляется

**Решение:** Проверьте переменные окружения:
```powershell
heroku config:get EMAIL_HOST_PASSWORD
```

Убедитесь, что используется пароль приложения Yandex, а не обычный пароль.

## Готово! 🎉

После выполнения всех шагов ваше приложение будет доступно по адресу:
`https://your-app-name.herokuapp.com`

