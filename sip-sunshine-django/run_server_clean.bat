@echo off
REM Clear Django cache and run server on port 3000
cd /d "%~dp0"

echo.
echo ======================================================
echo Sip and SunShine Restaurant - Development Server
echo ======================================================
echo.
echo Clearing cache...
if exist db.sqlite3-journal del db.sqlite3-journal
if exist staticfiles rmdir /s /q staticfiles >nul 2>&1

echo Collecting static files...
F:/sunshine/.venv/Scripts/python.exe manage.py collectstatic --noinput --clear >nul 2>&1

echo.
echo Starting development server...
echo ======================================================
echo.
echo Frontend: http://127.0.0.1:3000/
echo Admin:    http://127.0.0.1:3000/admin/
echo.
echo Username: admin
echo Password: admin123456
echo.
echo Press Ctrl+C to stop the server
echo ======================================================
echo.

F:/sunshine/.venv/Scripts/python.exe manage.py runserver 3000
