#! /usr/bin/bash

python manage.py makemigrations
python manage.py migrate --run-syncdb
python manage.py createsuperuser --no-input
python manage.py runserver 0.0.0.0:8000
