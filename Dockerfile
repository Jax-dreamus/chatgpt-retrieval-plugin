FROM python:3.10

WORKDIR /app

COPY . /app

ENV PYTHONPATH "${PYTHONPATH}:/app"

RUN pip install -r requirements.txt