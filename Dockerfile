# syntax=docker/dockerfile:1

FROM python:3.9-alpine

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install --upgrade -r requirements.txt

COPY . .

CMD [ "python3", "src/airdrops/main.py"]
