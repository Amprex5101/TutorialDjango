FROM python:3.10.4-alpine3.15
WORKDIR /

RUN apk add --no-cache \
    postgresql-dev \
    gcc \
    musl-dev \
    linux-headers \
    libffi-dev \
    python3-dev



COPY ./requirements.txt ./

RUN pip install -r requirements.txt

COPY ./ ./


CMD ["python3", "manage.py", "runserver", "127.0.0.2:3000"]
