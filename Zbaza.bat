@echo off
REM Change to your Django project directory (adjust if needed)
cd /d D:\zbaza

REM Activate virtual environment
call env\Scripts\activate.bat

REM Run Django development server on all interfaces port 8000
python manage.py runserver 0.0.0.0:8000

REM Keep the window open after server stops
pause