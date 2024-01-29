FROM ubuntu:latest
LABEL authors="jumacp"

RUN apt-get update
RUN apt-get install python-is-python3 python3-pip -y
RUN pip install --upgrade pip
WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

COPY ./laplacian_mechanisms.py /app

CMD python laplacian_mechanisms.py