#!/bin/sh

# run this from inside your container.
# Although *inside* the container the web server runs at 0.0.0.0:8000,
# from outside it appears at 127.0.0.1:8000.

./manage.py runserver 0.0.0.0:127
