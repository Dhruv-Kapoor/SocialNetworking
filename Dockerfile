FROM python:3.10-slim-bullseye

COPY . .

RUN pip install pipenv
RUN pipenv install --system --deploy

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

ENTRYPOINT ./entrypoint.sh
