@echo off
REM Quick Start Script for Sip and SunShine Django Project (Windows)

echo ==========================================
echo Sip and SunShine - Django Setup Script
echo ==========================================

REM Check if virtual environment exists
if not exist "venv" (
    echo.
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install requirements
echo.
echo Installing Python dependencies...
pip install -r requirements.txt

REM Run migrations
echo.
echo Running database migrations...
python manage.py migrate

REM Initialize database
echo.
echo Initializing database with sample data...
python setup_db.py

REM Summary
echo.
echo ==========================================
echo Setup Complete!
echo ==========================================
echo.
echo Next steps:
echo 1. Create superuser: python manage.py createsuperuser
echo 2. Run dev server: python manage.py runserver
echo 3. Visit: http://localhost:8000/admin
echo.
pause
