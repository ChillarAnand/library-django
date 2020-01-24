# Dockerfile
FROM python:3.7

# Setting PYTHONUNBUFFERED=1 avoids some stdout log anomalies.
ENV PYTHONUNBUFFERED=1

# Add ca-certificates as suggested by Aptible for SSL issue
RUN apt-get update && \
    apt-get install -y apt-transport-https ca-certificates vim && \
    curl -sS https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add - && \
    echo "deb http://apt.postgresql.org/pub/repos/apt/ stretch-pgdg main" | tee /etc/apt/sources.list.d/pgdg.list && \
    rm -rf /var/lib/apt/lists/*

# PostgreSQL dev headers and client
RUN apt-get update && \
    apt-get install -y libpq-dev postgresql-client-9.6 && \
    rm -rf /var/lib/apt/lists/*

ADD https://letsencrypt.org/certs/isrgrootx1.pem.txt /usr/local/share/ca-certificates/isrg_root.crt
ADD https://letsencrypt.org/certs/letsencryptauthorityx3.pem.txt /usr/local/share/ca-certificates/lets_encrypt_int.crt
RUN chmod 644 /usr/local/share/ca-certificates/isrg_root.crt /usr/local/share/ca-certificates/lets_encrypt_int.crt
RUN update-ca-certificates --fresh

ADD . /app
WORKDIR /app

# Build argument and environment variable to control installation of dev packages
ARG PIPENV_DEV=false
ENV PIPENV_DEV=$PIPENV_DEV

# Install python requirements
RUN set -ex && pip install --upgrade pip && \
    pip install pipenv && \
    pipenv install --system --deploy --ignore-pipfile

# Set shell
ENV SHELL=/bin/bash

RUN python manage.py collectstatic --noinput


# Set and expose default port
ENV PORT 8000
EXPOSE 8000

RUN python manage.py runserver 0:8000
