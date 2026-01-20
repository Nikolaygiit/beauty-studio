# ⚡ Быстрый деплой на GitHub Pages (5 минут)

## Способ 1: Автоматический (рекомендуется)

1. **Установите Git** (если еще не установлен):
   - Скачайте: https://git-scm.com/download/win
   - Установите с настройками по умолчанию

2. **Откройте PowerShell в папке проекта:**
   - Правый клик на папке "Проект 2" → "Открыть в PowerShell"
   - Или откройте PowerShell и перейдите: `cd "C:\Users\User\Desktop\Курсор\Проект 2"`

3. **Запустите скрипт:**
   ```powershell
   .\deploy.ps1
   ```

4. **Следуйте инструкциям на экране:**
   - Скрипт сам инициализирует Git
   - Попросит URL вашего GitHub репозитория
   - Загрузит файлы на GitHub

5. **Включите GitHub Pages:**
   - Откройте ваш репозиторий на GitHub
   - Settings → Pages
   - Branch: `main`, Folder: `/ (root)`
   - Save

6. **Готово!** Сайт будет доступен через 1-2 минуты.

---

## Способ 2: Через GitHub Desktop (самый простой)

1. **Установите GitHub Desktop:**
   - https://desktop.github.com/
   - Войдите в свой GitHub аккаунт

2. **Добавьте репозиторий:**
   - File → Add Local Repository
   - Выберите папку "Проект 2"
   - Нажмите "Publish repository"

3. **Включите GitHub Pages:**
   - Откройте репозиторий на GitHub.com
   - Settings → Pages
   - Branch: `main`, Folder: `/ (root)`
   - Save

4. **Готово!**

---

## Способ 3: Вручную через командную строку

Если у вас уже есть GitHub репозиторий:

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/ВАШ_USERNAME/ИМЯ_РЕПОЗИТОРИЯ.git
git push -u origin main
```

Затем включите Pages в настройках репозитория.

---

## ❓ Нужна помощь?

Откройте файл `DEPLOY.md` для подробной инструкции со скриншотами и решением проблем.
