ARG PYTHON_VERSION=3.11-slim-bullseye

FROM python:${PYTHON_VERSION}

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies.
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /code

WORKDIR /code

COPY requirements.txt /tmp/requirements.txt
RUN set -ex && \
    pip install --upgrade pip && \
    pip install -r /tmp/requirements.txt && \
    rm -rf /root/.cache/
COPY . /code

RUN python manage.py makemigrations
RUN python manage.py migrate
ENV DJANGO_SUPERUSER_USERNAME="admin"
ENV DJANGO_SUPERUSER_EMAIL="admin@admin.com"
ENV DJANGO_SUPERUSER_PASSWORD="admin"
RUN python manage.py ensure_adminuser --no-input

EXPOSE 8000

CMD ["gunicorn", "--bind", ":8000", "--workers", "2", "setup.wsgi"]
