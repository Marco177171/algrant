FROM python:latest

WORKDIR /usr/src/app

COPY . .

RUN pip install --upgrade pip
RUN pip install django psycopg pywebpush daphne channels channels-redis
RUN sh wait-for-postgres.sh

CMD [ "sh", "start-django-app.sh" ]