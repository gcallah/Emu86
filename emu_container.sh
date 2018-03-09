#!/bin/sh
docker run -it -p 8000:8000 -v $1:/home/Emu86 --name emu86 gcallah/emu86:v4 bash
