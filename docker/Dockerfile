FROM python:3.6.0

COPY requirements.txt /requirements.txt
COPY requirements-dev.txt /requirements-dev.txt

RUN pip install --upgrade pip

RUN pip install -r requirements.txt
RUN pip install -r requirements-dev.txt

WORKDIR /home/Emu86/
