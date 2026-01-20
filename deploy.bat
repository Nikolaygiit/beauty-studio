@echo off
chcp 65001 >nul
echo Выгрузка изменений на GitHub...
echo.

git add .
git commit -m "Update: Beauty Studio website"
git pull origin main --rebase
git push origin main

echo.
echo Готово! Изменения загружены на GitHub.
echo Сайт обновится через 1-2 минуты: https://nikolaygiit.github.io/beauty-studio/
pause
