FROM python:3.10

WORKDIR /tmp

COPY ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

CMD ["sh", "-c", "uvicorn server.main:app --host 0.0.0.0 --port 8080}"]
