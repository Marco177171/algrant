NAME=AlgrantApp

$(NAME):
	python ./django_app/manage.py runserver

migrations:
	python ./django_app/manage.py makemigrations
	python ./django_app/manage.py migrate
	python ./django_app/manage.py createsuperuser

clean:
	rm -rf algrantapp/db.sqlite

re:	clean $(NAME)

#pure:
#	docker system prune -a
