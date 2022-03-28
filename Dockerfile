FROM python:3.7

RUN mkdir /app
ADD . /app
WORKDIR /app

RUN apt -y update

RUN apt update && apt install -y python3 python3-pip

RUN pip install -r requirements.txt

EXPOSE 5000

RUN python3 broadcast.py