FROM python:latest

WORKDIR /usr/src/app

COPY . .

RUN pip install django
RUN pip install psycopg
RUN pip install django-channels

RUN sh wait-for-postgres.sh

CMD [ "sh", "start-django-app.sh" ]
