NAME=AlgrantApp

$(NAME):
	docker compose up --build
# add -d for background

stop:
	docker compose stop

clean:
	docker compose down

re:	clean $(NAME)

free:
	docker rm algrant_django

#pure:
#	docker system prune -a
