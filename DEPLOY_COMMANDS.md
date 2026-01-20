# Команды для деплоя на GitHub Pages

## Быстрый деплой (после исправления rebase)

Выполните эти команды по порядку:

```powershell
cd "C:\Users\User\Desktop\Курсор\Проект 2"

# 1. Прервать незавершенный rebase
git rebase --abort

# 2. Синхронизировать с удаленным репозиторием
git pull origin main --allow-unrelated-histories

# 3. Добавить все изменения
git add .

# 4. Создать коммит
git commit -m "Update: Beauty Studio website"

# 5. Загрузить на GitHub
git push origin main
```

## Обычный деплой (когда все синхронизировано)

После первого успешного деплоя, для следующих обновлений используйте:

```powershell
cd "C:\Users\User\Desktop\Курсор\Проект 2"

git add .
git commit -m "Update: Beauty Studio website"
git pull origin main
git push origin main
```

## Если возникнут конфликты

Если `git pull` покажет конфликты:

```powershell
# Использовать вашу локальную версию
git checkout --ours .
git add .
git commit -m "Resolve conflicts: use local version"
git push origin main
```

## Проверка статуса

Чтобы проверить текущее состояние:

```powershell
git status
git log --oneline -5
```
