#!/bin/sh
export HOST_PORT="8000"
export REPO=emu86
if [ $1 ]
then
    HOST_PORT=$1
fi

echo "Going to remove any lingering emu86-dev container."
docker rm emu86-dev 2> /dev/null || true
echo "Now running docker to spin up the container."
docker run -it -p $HOST_PORT:8000 -v $PWD:/home/Emu86 gcallah/$REPO-dev bash
