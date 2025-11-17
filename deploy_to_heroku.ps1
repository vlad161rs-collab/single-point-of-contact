# PowerShell скрипт для развёртывания на Heroku

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Развёртывание Django проекта на Heroku" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Проверка входа в Heroku
Write-Host "Проверка входа в Heroku..." -ForegroundColor Yellow
$herokuLoggedIn = heroku auth:whoami 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "✗ Вы не вошли в Heroku" -ForegroundColor Red
    Write-Host "  Выполните: heroku login" -ForegroundColor Yellow
    exit 1
}
Write-Host "✓ Вход выполнен: $herokuLoggedIn" -ForegroundColor Green
Write-Host ""

# Имя приложения (Heroku требует lowercase и дефисы)
$appName = "single-point-of-contact"

Write-Host "Имя приложения: $appName" -ForegroundColor Cyan
Write-Host ""

# Проверка существования приложения
Write-Host "Проверка существования приложения..." -ForegroundColor Yellow
$appExists = heroku apps:info -a $appName 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Приложение '$appName' уже существует" -ForegroundColor Green
    heroku git:remote -a $appName
} else {
    Write-Host "Создание нового приложения Heroku: $appName..." -ForegroundColor Yellow
    $createOutput = heroku create $appName 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Приложение создано: $appName" -ForegroundColor Green
    } else {
        Write-Host "✗ Ошибка создания приложения" -ForegroundColor Red
        Write-Host $createOutput
        exit 1
    }
}

Write-Host ""

# Добавление PostgreSQL
Write-Host "Добавление PostgreSQL аддона..." -ForegroundColor Yellow
heroku addons:create heroku-postgresql:mini -a $appName
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ PostgreSQL добавлен" -ForegroundColor Green
} else {
    Write-Host "⚠️ Возможно, PostgreSQL уже добавлен или произошла ошибка" -ForegroundColor Yellow
}
Write-Host ""

# Генерация SECRET_KEY
Write-Host "Генерация SECRET_KEY..." -ForegroundColor Yellow
$secretKey = python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
Write-Host "✓ SECRET_KEY сгенерирован" -ForegroundColor Green
Write-Host ""

# Установка переменных окружения
Write-Host "Установка переменных окружения..." -ForegroundColor Yellow
heroku config:set SECRET_KEY="$secretKey" -a $appName
heroku config:set DEBUG=False -a $appName
heroku config:set EMAIL_HOST_USER="xok1611995@yandex.ru" -a $appName
heroku config:set EMAIL_HOST_PASSWORD="ohzoflhqidrkzfya" -a $appName
heroku config:set ADMIN_EMAIL="xok1611995@yandex.ru" -a $appName
Write-Host "✓ Переменные окружения установлены" -ForegroundColor Green
Write-Host ""

# Проверка Git репозитория
Write-Host "Проверка Git репозитория..." -ForegroundColor Yellow
if (-not (Test-Path .git)) {
    Write-Host "Инициализация Git репозитория..." -ForegroundColor Yellow
    git init
    Write-Host "✓ Git инициализирован" -ForegroundColor Green
}

# Добавление файлов
Write-Host "Добавление файлов в Git..." -ForegroundColor Yellow
git add .
Write-Host "✓ Файлы добавлены" -ForegroundColor Green
Write-Host ""

# Коммит
Write-Host "Создание коммита..." -ForegroundColor Yellow
$commitMessage = Read-Host "Введите сообщение коммита (или нажмите Enter для использования 'Initial deployment')"
if ([string]::IsNullOrWhiteSpace($commitMessage)) {
    $commitMessage = "Initial deployment"
}
git commit -m $commitMessage
if ($LASTEXITCODE -ne 0) {
    Write-Host "⚠️ Возможно, нет изменений для коммита" -ForegroundColor Yellow
}
Write-Host ""

# Развёртывание
Write-Host "Развёртывание на Heroku..." -ForegroundColor Yellow
Write-Host "Это может занять несколько минут..." -ForegroundColor Yellow
git push heroku main
if ($LASTEXITCODE -ne 0) {
    Write-Host "Попытка push в master..." -ForegroundColor Yellow
    git push heroku master
}

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "============================================================" -ForegroundColor Green
    Write-Host "✓ Развёртывание завершено!" -ForegroundColor Green
    Write-Host "============================================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Следующие шаги:" -ForegroundColor Yellow
    Write-Host "1. Примените миграции:"
    Write-Host "   heroku run python manage.py migrate -a $appName"
    Write-Host ""
    Write-Host "2. Создайте суперпользователя:"
    Write-Host "   heroku run python manage.py createsuperuser -a $appName"
    Write-Host ""
    Write-Host "3. Соберите статические файлы:"
    Write-Host "   heroku run python manage.py collectstatic --noinput -a $appName"
    Write-Host ""
    Write-Host "4. Откройте приложение:"
    Write-Host "   heroku open -a $appName"
    Write-Host ""
} else {
    Write-Host ""
    Write-Host "============================================================" -ForegroundColor Red
    Write-Host "✗ Ошибка при развёртывании" -ForegroundColor Red
    Write-Host "============================================================" -ForegroundColor Red
    Write-Host ""
    Write-Host "Проверьте логи: heroku logs --tail -a $appName" -ForegroundColor Yellow
}
