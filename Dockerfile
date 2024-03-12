FROM python:3.11
WORKDIR /korean_site

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install poetry
COPY ./pyproject.toml .
RUN poetry install
COPY . .
