# ✅ Настройка PostgreSQL завершена!

## Что было сделано:

1. ✅ **Зависимости установлены** - все пакеты из `requirements.txt` установлены
2. ✅ **Переменная окружения установлена** - `DATABASE_URL` настроен
3. ✅ **Миграции применены** - все таблицы созданы в PostgreSQL

## Текущий статус:

- **База данных**: `django_knowledgebase`
- **Пользователь**: `postgres`
- **Хост**: `localhost:5432`
- **Подключение**: ✅ Работает

## Следующие шаги:

### 1. Создание суперпользователя

Выполните в PowerShell (в той же сессии, где установлен DATABASE_URL):

```powershell
python manage.py createsuperuser
```

Следуйте инструкциям на экране:
- Username: (введите имя пользователя)
- Email: (введите email, можно оставить пустым)
- Password: (введите пароль, минимум 8 символов)

### 2. Проверка работы

Запустите сервер разработки:

```powershell
python manage.py runserver
```

Откройте браузер и перейдите на:
- http://127.0.0.1:8000/ - главная страница
- http://127.0.0.1:8000/admin/ - админ-панель

### 3. Постоянная настройка DATABASE_URL (опционально)

Чтобы не устанавливать `DATABASE_URL` каждый раз, добавьте в файл `.env`:

```
DATABASE_URL=postgresql://postgres:1995@localhost:5432/django_knowledgebase
```

Или установите переменную окружения системы:
1. Панель управления → Система → Дополнительные параметры системы
2. Переменные среды → Новый (пользователь)
3. Имя: `DATABASE_URL`
4. Значение: `postgresql://postgres:1995@localhost:5432/django_knowledgebase`

## Проверка подключения к базе данных

Для проверки подключения выполните:

```powershell
python manage.py dbshell
```

Если подключение успешно, вы увидите приглашение PostgreSQL (`django_knowledgebase=#`). 
Введите `\q` для выхода.

## Полезные команды

```powershell
# Просмотр всех миграций
python manage.py showmigrations

# Создание новых миграций (если изменили модели)
python manage.py makemigrations

# Применение миграций
python manage.py migrate

# Сброс базы данных (ОСТОРОЖНО! Удалит все данные)
python manage.py flush

# Создание резервной копии данных
python manage.py dumpdata > backup.json

# Восстановление данных из резервной копии
python manage.py loaddata backup.json
```

## Готово к работе! 🎉

Теперь ваш проект использует PostgreSQL вместо SQLite и готов к развёртыванию на Heroku!

