FROM python:3.11.4-slim
WORKDIR /code

# variáveis para desenvolvimento
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV PYTHONPATH /code

RUN pip install --upgrade pip && \
    pip install poetry && \
    poetry config virtualenvs.create false

# Instala apenas as dependências.
COPY ./brain .
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root --only main

COPY ./brain/start-django /start-django
RUN sed -i 's/\r$//g' /start-django
RUN chmod +x /start-django
