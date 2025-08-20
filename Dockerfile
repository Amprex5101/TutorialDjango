FROM python:3.8-slim

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /app
WORKDIR /app
COPY ./requirements.txt /

# install psycopg2 dependencies
RUN apt-get update && apt-get install -y postgresql-client postgresql-server-dev-all gcc python3-dev libcurl4-openssl-dev libssl-dev swig python3-magic libmagic1
RUN apt install -y build-essential

RUN pip install --upgrade pip
RUN pip install -r /requirements.txt

COPY . /app



