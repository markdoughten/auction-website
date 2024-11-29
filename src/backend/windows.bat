@echo off
call .venv\Scripts\activate

set FLASK_ENV=development
set FLASK_DEBUG=1
set FLASK_APP=app.py

flask run
pause
