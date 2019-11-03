#!/bin/sh
export HOST_PORT="8000"
export CONT_PORT="8000"
export REPO="emu86"
export DH_ACCOUNT="gcallah"
export CONTAINER="$DH_ACCOUNT/$REPO"
if [ $1 ]
then
    HOST_PORT=$1
fi

echo "Going to remove any lingering indra container."
docker rm $REPO 2> /dev/null || true
echo "Now running docker to spin up the container."
docker run -it -p $HOST_PORT:$CONT_PORT $CONTAINER /home/$REPO/runserver.sh
