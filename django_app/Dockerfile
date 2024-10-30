FROM python:latest

WORKDIR /usr/src/app

COPY . .

RUN pip install django psycopg pywebpush
RUN sh wait-for-postgres.sh

CMD [ "sh", "start-django-app.sh" ]
