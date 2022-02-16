FROM python:3.8.3-alpine

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1

COPY . .

ARG name

RUN pip install --upgrade pip
RUN apk update \
    && apk add gcc musl-dev python3-dev libffi-dev openssl-dev cargo \
    && apk update && apk add postgresql-dev gcc python3-dev musl-dev \
    && apk add --virtual build-deps \
    && apk add jpeg-dev zlib-dev libjpeg \
    && pip install Pillow \
    && apk del build-deps

RUN pip install -r requirements.txt