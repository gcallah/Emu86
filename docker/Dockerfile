FROM python:3.6.0

ENV PROJECT Emu86

COPY requirements.txt /requirements.txt
COPY requirements-dev.txt /requirements-dev.txt

RUN pip install --upgrade pip

RUN pip install -r requirements-dev.txt

WORKDIR /home/$PROJECT/

RUN apt-get update
RUN apt-get install -y vim
