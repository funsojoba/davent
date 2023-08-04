FROM python:3.8.0-slim as builder

WORKDIR /app

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt .

RUN apt-get update \
    && apt-get install gcc python-dev libpq-dev postgresql-client -y \
    && apt-get install wkhtmltopdf -y \
    && apt-get install wget -y \
    && apt-get install python3-cffi python3-brotli libpango-1.0-0 libharfbuzz0b libpangoft2-1.0-0 \
    && apt-get update -y && apt-get upgrade -y && apt-get install -y --no-install-recommends binutils libproj-dev gdal-bin libgdal-dev python3-gdal \
    && apt-get clean

RUN pip install --upgrade pip \
    && pip install -r requirements.txt

COPY . .

CMD gunicorn CORE.wsgi:application --bind 0.0.0.0:$PORT
