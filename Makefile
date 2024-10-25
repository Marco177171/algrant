NAME=AlgrantApp

$(NAME):
<<<<<<< HEAD
	docker compose up --build -d
# add -d for background

stop:
	docker compose stop
=======
	pip install -r require.txt
	python ./django_app/manage.py makemigrations && python ./django_app/manage.py migrate --run-syncdb
	python ./django_app/manage.py runserver
>>>>>>> dev

clean:
	rm -rf django_app/db.sqlite3
	rm -rf django_app/algrant/__pycache__/*
	rm -rf django_app/algrantapp/__pycache__/*
	rm -rf django_app/algrantapp/migrations/*

re:	clean $(NAME)
