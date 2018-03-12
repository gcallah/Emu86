#!/bin/sh
if [ -z "$1" ]
  then
    echo "You must provide the location of your Emu86 repo."
    exit 1
fi
docker run -it -p 8000:8000 -v $1:/home/Emu86 --name emu86 gcallah/emu86:v4 bash
