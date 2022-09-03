FROM python:3.8.0-slim as builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# ENV DEBUG 1

COPY ./requirements.txt .

RUN pip install --upgrade pip \
    && pip install -r requirements.txt

COPY . .



CMD gunicorn CORE.wsgi:application --bind 0.0.0.0:$PORT
