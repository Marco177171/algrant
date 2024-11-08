NAME=AlgrantApp

$(NAME):
	python ./django_app/manage.py collectstatic
	daphne django_app.algrant.asgi:application

migrations:
	python ./django_app/manage.py makemigrations
	python ./django_app/manage.py migrate --run-syncdb
	python ./django_app/manage.py createsuperuser

clean:
	rm -rf ./django_app/db.sqlite3

re:	clean $(NAME)