# Простая выгрузка на GitHub

## Способ 1: Через батник (самый простой)

Просто дважды кликните на файл `deploy.bat` в папке проекта.

## Способ 2: Через PowerShell

Откройте PowerShell в папке проекта и выполните:

```powershell
cd "C:\Users\User\Desktop\Курсор\Проект 2"

git add .
git commit -m "Update: Beauty Studio website"
git pull origin main --rebase
git push origin main
```

## Если возникнут ошибки

**Ошибка с rebase:**
```powershell
git rebase --abort
git pull origin main --allow-unrelated-histories
git push origin main
```

**Ошибка "non-fast-forward":**
```powershell
git pull origin main --allow-unrelated-histories
git push origin main
```

**Принудительная загрузка (если уверены в своей версии):**
```powershell
git push origin main --force
```

## После успешной загрузки

Сайт автоматически обновится через 1-2 минуты:
**https://nikolaygiit.github.io/beauty-studio/**
