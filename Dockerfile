FROM python:3.12.5-alpine3.20

LABEL org.opencontainers.image.authors="sudip@firstcontainer.com"

ENV PYTHONUNBUFFERED 1

COPY ./requirement.txt /requirements.txt
RUN pip install -r /requirements.txt

RUN MKDIR /app
WORKDIR /app
COPY ./base app

RUN adduser -D user
USER user