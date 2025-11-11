#/bin/sh

# Once you have gotten the source code and setup the virtual env,
# run this script (once!).

make prod_env
./db.sh
./manage.py createsuperuser
