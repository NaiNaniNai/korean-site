FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /korean_site
COPY . /korean_site/
RUN pip install poetry
RUN poetry install
