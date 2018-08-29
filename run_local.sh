#!/bin/sh
docker rm emu86 || true
# we shouldn't need -it here:
docker run -p 8000:8000 -v /tmp/Haldun:/home/Emu86 --name emu86 gcallah/emu86:v4 /home/Emu86/manage.py runserver 0.0.0.0:8000
