# Исправление ошибки 400 Bad Request

## Проблема:
Ошибка 400 из-за неправильной настройки ALLOWED_HOSTS

## Решение:

### Шаг 1: Перейдите в директорию проекта

```powershell
cd "D:\Росдистант\Информатика\3 курс 1 семестр\Производственная практика (преддипломная практика)\djangoProject"
```

### Шаг 2: Установите ALLOWED_HOSTS через переменную окружения (самый быстрый способ)

```powershell
heroku config:set ALLOWED_HOSTS=".herokuapp.com,single-point-of-contact-570955226190.herokuapp.com" -a single-point-of-contact
```

### Шаг 3: Перезапустите приложение

```powershell
heroku restart -a single-point-of-contact
```

### Шаг 4: Проверьте работу

Откройте: https://single-point-of-contact-570955226190.herokuapp.com/

### Альтернатива: Закоммитьте изменения

Если хотите закоммитить изменения в settings.py:

```powershell
cd "D:\Росдистант\Информатика\3 курс 1 семестр\Производственная практика (преддипломная практика)\djangoProject"
git add djangoProject/settings.py
git commit -m "Fix ALLOWED_HOSTS for Heroku"
git push heroku master
```

Но проще использовать переменную окружения (шаг 2).

