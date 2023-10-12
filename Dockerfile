FROM python:3.8.0-slim as builder

WORKDIR /app

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt .

RUN apt-get update && apt-get install -y \
    gcc python-dev libpq-dev postgresql-client wkhtmltopdf wget python3-cffi python3-brotli \
    libpango-1.0-0 libharfbuzz0b libpangoft2-1.0-0 --no-install-recommends \
    binutils libproj-dev libgdal-dev && \
    apt-get clean

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

CMD gunicorn CORE.wsgi:application --bind 0.0.0.0:$PORT
