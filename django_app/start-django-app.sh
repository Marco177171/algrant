python manage.py makemigrations
python manage.py migrate --run-syncdb
python manage.py collectstatic
# python manage.py createsuperuser --no-input
# python manage.py runserver 0.0.0.0:8000
daphne -b 0.0.0.0 -p 8000 algrant.asgi:application
