# 🚀 Развёртывание на Heroku - Пошаговая инструкция

## ✅ Подготовка завершена!

- ✅ Статические файлы собраны (165 файлов)
- ✅ Git репозиторий инициализирован
- ✅ SECRET_KEY сгенерирован
- ✅ Все файлы готовы

## Шаг 1: Вход в Heroku

```powershell
heroku login
```

Откроется браузер для авторизации. Войдите в свой аккаунт Heroku.

## Шаг 2: Создание приложения Heroku

```powershell
# Вариант A: Автоматическое создание (Heroku выберет имя)
heroku create

# Вариант B: С указанием имени (должно быть уникальным)
heroku create your-app-name
```

**Важно:** Имя приложения должно быть уникальным и содержать только строчные буквы, цифры и дефисы.

## Шаг 3: Добавление PostgreSQL

```powershell
heroku addons:create heroku-postgresql:mini
```

Это создаст бесплатную базу данных PostgreSQL на Heroku.

## Шаг 4: Установка переменных окружения

```powershell
# Получите имя вашего приложения (замените your-app-name)
$appName = "your-app-name"

# Генерация SECRET_KEY
$secretKey = python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Установка переменных
heroku config:set SECRET_KEY="$secretKey" -a $appName
heroku config:set DEBUG=False -a $appName
heroku config:set EMAIL_HOST_USER="xok1611995@yandex.ru" -a $appName
heroku config:set EMAIL_HOST_PASSWORD="ohzoflhqidrkzfya" -a $appName
heroku config:set ADMIN_EMAIL="xok1611995@yandex.ru" -a $appName
```

## Шаг 5: Подготовка Git репозитория

```powershell
# Добавление всех файлов
git add .

# Создание коммита
git commit -m "Initial deployment to Heroku"

# Добавление удалённого репозитория Heroku (если ещё не добавлен)
heroku git:remote -a your-app-name
```

## Шаг 6: Развёртывание

```powershell
# Отправка кода на Heroku
git push heroku main

# Если main не работает, попробуйте:
git push heroku master
```

Это займёт несколько минут. Heroku автоматически:
- Установит все зависимости из `requirements.txt`
- Соберёт статические файлы (если настроено)
- Запустит приложение

## Шаг 7: Применение миграций

```powershell
heroku run python manage.py migrate -a your-app-name
```

## Шаг 8: Создание суперпользователя

```powershell
heroku run python manage.py createsuperuser -a your-app-name
```

Следуйте инструкциям на экране.

## Шаг 9: Сбор статических файлов

```powershell
heroku run python manage.py collectstatic --noinput -a your-app-name
```

## Шаг 10: Открытие приложения

```powershell
heroku open -a your-app-name
```

Или перейдите по адресу: `https://your-app-name.herokuapp.com`

## Полезные команды

```powershell
# Просмотр логов
heroku logs --tail -a your-app-name

# Просмотр переменных окружения
heroku config -a your-app-name

# Перезапуск приложения
heroku restart -a your-app-name

# Масштабирование (если нужно)
heroku ps:scale web=1 -a your-app-name

# Выполнение команд Django
heroku run python manage.py <command> -a your-app-name
```

## Автоматический скрипт

Для автоматизации процесса можно использовать скрипт:

```powershell
powershell -ExecutionPolicy Bypass -File deploy_to_heroku.ps1
```

Скрипт проведёт вас через все шаги интерактивно.

## Проверка после развёртывания

После развёртывания проверьте:

1. ✅ Главная страница открывается
2. ✅ Статические файлы загружаются (CSS, изображения)
3. ✅ Вход в систему работает
4. ✅ Админ-панель доступна
5. ✅ Создание заявок работает
6. ✅ Email уведомления работают

## Решение проблем

### Проблема: "No app specified"
**Решение:** Укажите имя приложения: `-a your-app-name`

### Проблема: Статические файлы не загружаются
**Решение:** 
```powershell
heroku run python manage.py collectstatic --noinput -a your-app-name
```

### Проблема: Ошибка базы данных
**Решение:**
```powershell
heroku run python manage.py migrate -a your-app-name
```

### Проблема: Email не отправляется
**Решение:** Проверьте переменные окружения:
```powershell
heroku config -a your-app-name
```

Убедитесь, что `EMAIL_HOST_PASSWORD` установлен правильно (пароль приложения Yandex).

## Готово! 🎉

Ваше приложение должно быть доступно по адресу:
**https://your-app-name.herokuapp.com**

