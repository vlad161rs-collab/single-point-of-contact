# Исправление проблем с отделами и медиа файлами

## Проблема 1: Отделы не выбираются

### Причина:
Возможно, в базе данных нет отделов, или проблема с отображением формы.

### Решение:

1. **Создайте отделы в базе данных:**

В Heroku Console выполните:
```bash
python manage.py create_departments
```

Или создайте отделы вручную через админ-панель или Django shell:
```python
from portal.models import Department
Department.objects.get_or_create(name="IT отдел")
Department.objects.get_or_create(name="Отдел поддержки")
Department.objects.get_or_create(name="Администрация")
```

2. **Проверьте, что отделы есть в базе:**
```bash
python manage.py shell
```

Затем:
```python
from portal.models import Department
print(Department.objects.all())
```

## Проблема 2: Медиа файлы (картинки, аудио, видео) не открываются

### Причина:
На Heroku файловая система эфемерна - медиа файлы теряются при перезапуске приложения.

### Решение:

**ВАЖНО:** На Heroku медиа файлы НЕ сохраняются между перезапусками!

#### Вариант 1: Временное решение (для тестирования)

Я настроил базовую раздачу медиа файлов. Но помните:
- Файлы будут потеряны при перезапуске приложения
- Это не подходит для продакшена

#### Вариант 2: Облачное хранилище (рекомендуется для продакшена)

Используйте один из сервисов:
- **AWS S3** (Amazon Simple Storage Service)
- **Cloudinary** (проще в настройке)
- **Google Cloud Storage**
- **Azure Blob Storage**

### Настройка Cloudinary (самый простой вариант):

1. Зарегистрируйтесь на https://cloudinary.com
2. Установите пакет:
```bash
pip install django-cloudinary-storage
```

3. Добавьте в `requirements.txt`:
```
django-cloudinary-storage==0.3.0
```

4. Обновите `settings.py`:
```python
INSTALLED_APPS = [
    # ...
    'cloudinary_storage',
    'django.contrib.staticfiles',
    'cloudinary',
    # ...
]

# Cloudinary настройки
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': 'your-cloud-name',
    'API_KEY': 'your-api-key',
    'API_SECRET': 'your-api-secret'
}

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
```

5. Установите переменные окружения на Heroku:
```bash
heroku config:set CLOUDINARY_URL="cloudinary://api_key:api_secret@cloud_name" -a single-point-of-contact
```

## Что нужно сделать сейчас:

1. **Создайте отделы:**
```bash
heroku run python manage.py create_departments -a single-point-of-contact
```

2. **Закоммитьте и разверните изменения:**
```bash
git add .
git commit -m "Fix departments selection and media files"
git push heroku master
```

3. **Проверьте работу:**
- Откройте форму регистрации - отделы должны выбираться
- Откройте личный кабинет - отделы должны выбираться
- Попробуйте загрузить новую картинку в статью (она будет работать до перезапуска)

## Важно для медиа файлов:

Для продакшена обязательно настройте облачное хранилище, иначе все загруженные файлы будут потеряны при перезапуске Heroku!

