Docker Compose
==============
![Docker Compose](https://raw.githubusercontent.com/docker/compose/master/logo.png "Docker Compose Logo")

# Overview: 
This docker compose file builds the Emu86 image as defined in the Dockerfile. 
It also maps the respository root directory on the host to the work directory 
in the container and runs the django application on port 8000. Any changes 
made locally is reflected on http://localhost:8000 as port 8000 in the 
container is mapped to port 8000 on the Docker host.
 
To start Emu86 application on docker ('-d' for detached):

    docker-compose up -d
To stop the deployed Emu86 application:

    docker-compose down