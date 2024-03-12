FROM python:3.11
WORKDIR /korean_site

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN curl -sSL https://install.python-poetry.org | python3 -
COPY ./pyproject.toml .
RUN /root/.local/bin/poetry install
COPY . .
RUN pip install django environ django-environ django_migration_linter django-ckeditor django-silk psycopg2 Pillow
