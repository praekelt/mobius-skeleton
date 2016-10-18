#!/bin/bash

echo "Ensuring required system libraries are installed. You may be prompted for your password."
sudo apt-get install python-virtualenv python-dev \
libjpeg-dev zlib1g-dev build-essential git-core \
sqlite libxslt1-dev --no-upgrade

echo "Setting up sandboxed Python environment."
rm -rf ve
virtualenv ve
./ve/bin/pip install -r requirements/requirements.txt
./ve/bin/python manage.py migrate
./ve/bin/python manage.py load_photosizes
./ve/bin/python manage.py createsuperuser

echo "You may now start up the site with ./ve/bin/python manage.py runserver 0.0.0.0:8000"
echo "Browse to http://localhost:8000/ for the public site."
echo "Browse to http://localhost:8000/admin/ for the admin interface."
