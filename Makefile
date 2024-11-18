NAME=AlgrantApp

$(NAME):
	./django_app/manage.py makemigrations
	./django_app/manage.py migrate --run-syncdb
	# ./django_app/manage.py createsuperuser --no-input
	daphne -b 0.0.0.0 -p 8000 django_app.algrant.asgi:application

clean:
	rm -rf django_app/algrant/__pycache__/*
	rm -rf django_app/algrantapp/__pycache__/*

clean_all: clean
	rm -rf django_app/db.sqlite3

re:	clean_all $(NAME)