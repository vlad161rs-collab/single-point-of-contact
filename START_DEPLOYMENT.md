# 🚀 Начните развёртывание на Heroku!

## ✅ Всё готово к развёртыванию!

Проект полностью подготовлен:
- ✅ Статические файлы собраны
- ✅ Git репозиторий готов
- ✅ Все необходимые файлы добавлены
- ✅ Конфигурация для Heroku настроена

## Быстрый старт (3 команды)

### 1. Войдите в Heroku
```powershell
heroku login
```

### 2. Создайте приложение и разверните
```powershell
# Создание приложения (Heroku выберет имя автоматически)
heroku create

# Или с указанием имени (должно быть уникальным)
heroku create your-unique-app-name

# Развёртывание
git commit -m "Initial deployment"
git push heroku main
```

### 3. Настройте и запустите
```powershell
# Получите имя приложения из вывода предыдущей команды
# Замените 'your-app-name' на реальное имя

# Добавьте PostgreSQL
heroku addons:create heroku-postgresql:mini

# Установите переменные окружения
$secretKey = python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
heroku config:set SECRET_KEY="$secretKey"
heroku config:set DEBUG=False
heroku config:set EMAIL_HOST_USER="xok1611995@yandex.ru"
heroku config:set EMAIL_HOST_PASSWORD="ohzoflhqidrkzfya"
heroku config:set ADMIN_EMAIL="xok1611995@yandex.ru"

# Примените миграции
heroku run python manage.py migrate

# Создайте суперпользователя
heroku run python manage.py createsuperuser

# Соберите статические файлы
heroku run python manage.py collectstatic --noinput

# Откройте приложение
heroku open
```

## Подробная инструкция

См. файл **HEROKU_DEPLOY.md** для пошаговой инструкции.

## Автоматический скрипт

Или используйте автоматический скрипт:
```powershell
powershell -ExecutionPolicy Bypass -File deploy_to_heroku.ps1
```

## Что дальше?

После развёртывания:
1. Проверьте работу приложения
2. Протестируйте все функции
3. Настройте мониторинг (опционально)
4. Настройте резервное копирование (опционально)

## Готово! 🎉

Ваше приложение будет доступно по адресу:
**https://your-app-name.herokuapp.com**

