# ✅ Финальный чеклист перед развёртыванием

## Проверка готовности

- [x] ✅ Все зависимости установлены (`requirements.txt`)
- [x] ✅ Статические файлы собраны (`collectstatic`)
- [x] ✅ Git репозиторий инициализирован
- [x] ✅ Все файлы добавлены в Git
- [x] ✅ `.gitignore` настроен правильно
- [x] ✅ `Procfile` создан
- [x] ✅ `runtime.txt` создан
- [x] ✅ `requirements.txt` содержит все зависимости
- [x] ✅ `settings.py` настроен для Heroku
- [x] ✅ PostgreSQL настроен локально
- [x] ✅ Миграции применены локально
- [x] ✅ Суперпользователь создан

## Перед развёртыванием

### 1. Проверьте Heroku CLI
```powershell
heroku --version
```
Должна быть установлена версия.

### 2. Войдите в Heroku
```powershell
heroku login
```

### 3. Создайте коммит
```powershell
git commit -m "Initial deployment to Heroku"
```

## Команды для развёртывания

### Создание приложения
```powershell
heroku create your-app-name
```

### Добавление PostgreSQL
```powershell
heroku addons:create heroku-postgresql:mini
```

### Установка переменных окружения
```powershell
$secretKey = python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
heroku config:set SECRET_KEY="$secretKey"
heroku config:set DEBUG=False
heroku config:set EMAIL_HOST_USER="xok1611995@yandex.ru"
heroku config:set EMAIL_HOST_PASSWORD="ohzoflhqidrkzfya"
heroku config:set ADMIN_EMAIL="xok1611995@yandex.ru"
```

### Развёртывание
```powershell
git push heroku main
```

### Применение миграций
```powershell
heroku run python manage.py migrate
```

### Создание суперпользователя
```powershell
heroku run python manage.py createsuperuser
```

### Сбор статических файлов
```powershell
heroku run python manage.py collectstatic --noinput
```

### Открытие приложения
```powershell
heroku open
```

## После развёртывания

Проверьте:
- [ ] Главная страница открывается
- [ ] Статические файлы загружаются
- [ ] Вход в систему работает
- [ ] Админ-панель доступна
- [ ] Создание заявок работает
- [ ] Email уведомления работают

## Готово! 🎉

