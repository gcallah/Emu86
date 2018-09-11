# Windows Powershell Script for DevOps Docker Container
docker rm devops | true
docker run -it -p 8000:8000 -v ${PWD}:/home/Emu86 emu86 bash
