NAME=AlgrantApp

$(NAME):
	docker compose up --build -d

stop:
	docker compose stop

clean:
	docker compose down

re:	clean $(NAME)

free:
	docker rm algrant_django

#pure:
#	docker system prune -a
