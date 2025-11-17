# Simple Heroku deployment script
$appName = "single-point-of-contact"

Write-Host "Deploying to Heroku: $appName" -ForegroundColor Cyan
Write-Host ""

# Check Heroku login
Write-Host "Checking Heroku login..." -ForegroundColor Yellow
heroku auth:whoami
if ($LASTEXITCODE -ne 0) {
    Write-Host "Please login: heroku login" -ForegroundColor Red
    exit 1
}
Write-Host ""

# Create or use app
Write-Host "Checking app: $appName" -ForegroundColor Yellow
heroku apps:info -a $appName 2>&1 | Out-Null
if ($LASTEXITCODE -ne 0) {
    Write-Host "Creating app: $appName" -ForegroundColor Yellow
    heroku create $appName
} else {
    Write-Host "App exists, using: $appName" -ForegroundColor Green
    heroku git:remote -a $appName
}
Write-Host ""

# Add PostgreSQL
Write-Host "Adding PostgreSQL..." -ForegroundColor Yellow
heroku addons:create heroku-postgresql:mini -a $appName
Write-Host ""

# Generate SECRET_KEY
Write-Host "Generating SECRET_KEY..." -ForegroundColor Yellow
$secretKey = python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
Write-Host ""

# Set config vars
Write-Host "Setting config variables..." -ForegroundColor Yellow
heroku config:set SECRET_KEY="$secretKey" -a $appName
heroku config:set DEBUG=False -a $appName
heroku config:set EMAIL_HOST_USER="xok1611995@yandex.ru" -a $appName
heroku config:set EMAIL_HOST_PASSWORD="ohzoflhqidrkzfya" -a $appName
heroku config:set ADMIN_EMAIL="xok1611995@yandex.ru" -a $appName
Write-Host ""

# Git operations
Write-Host "Preparing Git..." -ForegroundColor Yellow
git add .
git commit -m "Deploy to Heroku - Single Point of Contact"
Write-Host ""

# Deploy
Write-Host "Deploying to Heroku..." -ForegroundColor Yellow
Write-Host "This may take a few minutes..." -ForegroundColor Yellow
git push heroku main
if ($LASTEXITCODE -ne 0) {
    git push heroku master
}

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "Deployment complete!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Yellow
    Write-Host "1. heroku run python manage.py migrate -a $appName"
    Write-Host "2. heroku run python manage.py createsuperuser -a $appName"
    Write-Host "3. heroku run python manage.py collectstatic --noinput -a $appName"
    Write-Host "4. heroku open -a $appName"
} else {
    Write-Host "Deployment failed. Check logs: heroku logs --tail -a $appName" -ForegroundColor Red
}

