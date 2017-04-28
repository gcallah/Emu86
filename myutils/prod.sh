#!/bin/bash
# for the dev server: fetches new code and restarts the server.

git pull origin master
touch /var/www/www_emu86_org_wsgi.py
