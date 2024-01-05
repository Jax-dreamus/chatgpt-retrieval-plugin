FROM python:3.10

WORKDIR /tmp

COPY ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
