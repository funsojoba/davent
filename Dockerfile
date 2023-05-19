FROM python:3.8.0-slim as builder

WORKDIR /app

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt .

RUN apt-get update \
    && apt-get install gcc python-dev libpq-dev postgresql-client -y \
    && apt-get clean

RUN pip install --upgrade pip \
    && pip install -r requirements.txt

COPY . .

CMD gunicorn CORE.wsgi:application --bind 0.0.0.0:$PORT
