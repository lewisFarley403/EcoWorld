python manage.py makemigrations
python manage.py migrate
python manage.py loaddata initialDb.json
python manage.py collectstatic --noinput
python manage.py createsuperuser
echo "Database setup complete!"
