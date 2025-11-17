# Исправление ошибки 500 на Render

## Шаг 1: Проверьте логи в Render

1. В Dashboard Render откройте ваш Web Service
2. Перейдите в **"Logs"**
3. Найдите ошибку (обычно в конце логов)
4. Скопируйте полный текст ошибки

## Шаг 2: Временное включение DEBUG

Я обновил settings.py, чтобы DEBUG был True по умолчанию. Это покажет детальную ошибку.

**В Render Dashboard:**
1. Откройте **Environment Variables**
2. Убедитесь, что `DEBUG=True` (или удалите переменную DEBUG)
3. Сохраните - Render автоматически пересоберёт

## Шаг 3: Применение миграций локально

Выполните в PowerShell:

```powershell
cd "D:\Росдистант\Информатика\3 курс 1 семестр\Производственная практика (преддипломная практика)\djangoProject"

# Установите DATABASE_URL
$env:DATABASE_URL="postgresql://single_point_of_contact_db_user:BESeJY4HZ1XrkQDSiuXxNmxyhvYlK2on@dpg-d4dplour433s7385okpg-a/single_point_of_contact_db"

# Примените миграции
python manage.py migrate

# Создайте отделы
python manage.py create_departments
```

## Шаг 4: Проверка переменных окружения

Убедитесь, что в Render установлены все переменные:

- ✅ SECRET_KEY (обязательно!)
- ✅ DATABASE_URL
- ✅ DEBUG=True (временно)
- ✅ ALLOWED_HOSTS=single-point-of-contact.onrender.com
- ✅ EMAIL_HOST_USER
- ✅ EMAIL_HOST_PASSWORD
- ✅ ADMIN_EMAIL

## Шаг 5: Проверка подключения к БД

После применения миграций проверьте:

```powershell
python manage.py dbshell
```

Если подключение успешно, вы увидите приглашение PostgreSQL.

## Частые причины ошибки 500:

1. **Миграции не применены** - выполните шаг 3
2. **SECRET_KEY не установлен** - проверьте переменные окружения
3. **DATABASE_URL неправильный** - проверьте формат
4. **ALLOWED_HOSTS не включает домен** - добавьте ваш домен Render
5. **Ошибка в коде** - проверьте логи с DEBUG=True

## После исправления:

1. Откройте сайт снова
2. Если ошибка исчезла, установите `DEBUG=False` в переменных окружения
3. Пересоберите приложение

