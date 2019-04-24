#!/bin/bash
# for the dev server: fetches new code and restarts the server.

echo "Getting new files from GitHub."
git pull origin master
echo "Rebooting serber."
touch /var/www/www_emu86_org_wsgi.py
