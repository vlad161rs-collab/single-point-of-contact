# Настройка PostgreSQL - Пошаговая инструкция

## Шаг 1: Создание базы данных

### Вариант A: Через pgAdmin 4 (рекомендуется)

1. Откройте **pgAdmin 4** (обычно устанавливается вместе с PostgreSQL)
2. Подключитесь к серверу PostgreSQL:
   - Пароль: `1995`
   - Если сервер не виден, добавьте его вручную:
     - Host: `localhost`
     - Port: `5432`
     - Username: `postgres`
     - Password: `1995`
3. В дереве слева найдите **Databases**
4. Правой кнопкой мыши на **Databases** → **Create** → **Database**
5. В открывшемся окне:
   - **Database name**: `django_knowledgebase`
   - **Encoding**: `UTF8`
   - Нажмите **Save**

### Вариант B: Через SQL команду

1. Откройте pgAdmin 4
2. Подключитесь к серверу PostgreSQL (пароль: `1995`)
3. Правой кнопкой на **postgres** (системная база) → **Query Tool**
4. Выполните команду:
   ```sql
   CREATE DATABASE django_knowledgebase WITH ENCODING='UTF8';
   ```
5. Нажмите **Execute** (F5)

## Шаг 2: Установка переменной окружения

Откройте PowerShell в директории проекта и выполните:

```powershell
$env:DATABASE_URL="postgresql://postgres:1995@localhost:5432/django_knowledgebase"
```

**Проверка:**
```powershell
echo $env:DATABASE_URL
```

Должно вывести: `postgresql://postgres:1995@localhost:5432/django_knowledgebase`

## Шаг 3: Применение миграций

В той же сессии PowerShell выполните:

```powershell
python manage.py migrate
```

## Шаг 4: Создание суперпользователя

```powershell
python manage.py createsuperuser
```

Следуйте инструкциям на экране.

## Проверка

После выполнения всех шагов проверьте подключение:

```powershell
python manage.py dbshell
```

Если подключение успешно, вы увидите приглашение PostgreSQL. Введите `\q` для выхода.

## Постоянная настройка (опционально)

Чтобы не устанавливать `DATABASE_URL` каждый раз, добавьте в файл `.env`:

```
DATABASE_URL=postgresql://postgres:1995@localhost:5432/django_knowledgebase
```

Или установите переменную окружения системы через:
1. Панель управления → Система → Дополнительные параметры системы
2. Переменные среды → Новый (пользователь)
3. Имя: `DATABASE_URL`
4. Значение: `postgresql://postgres:1995@localhost:5432/django_knowledgebase`

