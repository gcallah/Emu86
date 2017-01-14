#/bin/sh

# Once you have gotten the source code and setup the virtual env,
# run this script (once!).

#pip install django
pip install django-extensions
./db.sh
./manage.py createsuperuser
