#!/bin/sh
docker rm emu86 || true
docker run -it -p 8000:8000 -v $PWD:/home/Emu86 emu86 bash