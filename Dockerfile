# Dockerfile
FROM python:3.7

ENV PYTHONUNBUFFERED=1

ADD . /app
WORKDIR /app

RUN pip install -r requirements.txt

ENV SHELL=/bin/bash

RUN python manage.py collectstatic --noinput

ENV PORT 8000
EXPOSE 8000
