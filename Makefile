NAME=AlgrantApp

$(NAME):
	python ./algrantapp/manage.py runserver
# add -d for background

migrations:
	python ./algrantapp/manage.py makemigrations
	python ./algrantapp/manage.py migrate
	python ./algrantapp/manage.py createsuperuser

clean:
	rm -rf algrantapp/db.sqlite

re:	clean $(NAME)

#pure:
#	docker system prune -a
