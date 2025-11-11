#!/bin/bash
# for the dev server: fetches new code and restarts the server.

echo "Getting new files from GitHub."
git pull origin master
# activate our virtual env:
source /home/gcallah/.virtualenvs/django2/bin/activate
# install all of our packages:
make prod
echo "Rebooting server."
touch /var/www/www_emu86_org_wsgi.py
