@echo off
python manage.py makemigrations
python manage.py migrate
python manage.py loaddata initialDb.json
echo Database setup complete!
pause
