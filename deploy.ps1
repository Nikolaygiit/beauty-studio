# Скрипт для автоматизации деплоя на GitHub Pages
# Запустите: .\deploy.ps1

Write-Host "🚀 Подготовка к деплою на GitHub Pages..." -ForegroundColor Cyan

# Проверка Git
try {
    $gitVersion = git --version
    Write-Host "✓ Git установлен: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Git не найден. Установите Git: https://git-scm.com/download/win" -ForegroundColor Red
    exit 1
}

# Проверка, инициализирован ли репозиторий
if (-not (Test-Path .git)) {
    Write-Host "📦 Инициализация Git репозитория..." -ForegroundColor Yellow
    git init
    Write-Host "✓ Репозиторий инициализирован" -ForegroundColor Green
} else {
    Write-Host "✓ Git репозиторий уже существует" -ForegroundColor Green
}

# Добавление файлов
Write-Host "📝 Добавление файлов..." -ForegroundColor Yellow
git add .

# Проверка статуса
$status = git status --porcelain
if ($status) {
    Write-Host "📋 Изменения для коммита:" -ForegroundColor Yellow
    git status --short
    
    $commitMessage = Read-Host "Введите описание коммита (или нажмите Enter для стандартного)"
    if ([string]::IsNullOrWhiteSpace($commitMessage)) {
        $commitMessage = "Update: Beauty Studio website"
    }
    
    git commit -m $commitMessage
    Write-Host "✓ Изменения закоммичены" -ForegroundColor Green
} else {
    Write-Host "ℹ Нет изменений для коммита" -ForegroundColor Yellow
}

# Проверка remote
$remote = git remote get-url origin 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "⚠ GitHub remote не настроен" -ForegroundColor Yellow
    Write-Host ""
    $githubUrl = Read-Host "Введите URL вашего GitHub репозитория (например: https://github.com/username/repo.git)"
    if ($githubUrl) {
        git remote add origin $githubUrl
        Write-Host "✓ Remote добавлен" -ForegroundColor Green
    } else {
        Write-Host "✗ Remote не добавлен. Добавьте вручную: git remote add origin <URL>" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "✓ Remote настроен: $remote" -ForegroundColor Green
}

# Переименование ветки в main (если нужно)
$currentBranch = git branch --show-current
if ($currentBranch -ne "main") {
    Write-Host "🔄 Переименование ветки в main..." -ForegroundColor Yellow
    git branch -M main
    Write-Host "✓ Ветка переименована в main" -ForegroundColor Green
}

# Push
Write-Host ""
Write-Host "📤 Загрузка на GitHub..." -ForegroundColor Yellow
Write-Host "⚠ Если потребуется авторизация, используйте Personal Access Token вместо пароля" -ForegroundColor Yellow
Write-Host ""

git push -u origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✅ Код успешно загружен на GitHub!" -ForegroundColor Green
    Write-Host ""
    Write-Host "📋 Следующие шаги:" -ForegroundColor Cyan
    Write-Host "1. Откройте ваш репозиторий на GitHub" -ForegroundColor White
    Write-Host "2. Перейдите в Settings → Pages" -ForegroundColor White
    Write-Host "3. Выберите branch: main, folder: / (root)" -ForegroundColor White
    Write-Host "4. Нажмите Save" -ForegroundColor White
    Write-Host "5. Через 1-2 минуты сайт будет доступен по адресу:" -ForegroundColor White
    Write-Host "   https://ВАШ_USERNAME.github.io/ИМЯ_РЕПОЗИТОРИЯ/" -ForegroundColor Yellow
} else {
    Write-Host ""
    Write-Host "✗ Ошибка при загрузке. Проверьте:" -ForegroundColor Red
    Write-Host "  - Правильность URL репозитория" -ForegroundColor White
    Write-Host "  - Наличие прав доступа" -ForegroundColor White
    Write-Host "  - Использование Personal Access Token" -ForegroundColor White
}
