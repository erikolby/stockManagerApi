FROM python:3.9-alpine3.16

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
COPY ./portfoliomanager /portfoliomanager

WORKDIR /portfoliomanager
EXPOSE 8000

RUN python -m venv /venv && \
    /venv/bin/pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-deps \
        build-base postgresql-dev musl-dev && \
    /venv/bin/pip install -r /requirements.txt && \    
    apk del .tmp-deps && \
    adduser --disabled-password --no-create-home portfoliomanager

ENV PATH="/venv/bin:$PATH"

USER portfoliomanager
