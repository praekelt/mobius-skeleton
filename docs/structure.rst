Skeleton structure
==================

The skeleton contains a number of directories and files.

productname
-----------

Directory containing Django ``models.py``, migrations, fixtures, static files and tests.

conf
----

Directory containing templates for generating working Nginx and Supervisor
configuration files.

fed
---

Directory where front end developers can safely prototype static pages. Django itself
prefers the top level directory and this approach prevents collisions.

project
-------

Directory containing various settings files and ``urls.py`` for the project.

scripts
-------

Directory containing reference bash scripts to setup an Ubuntu 14.04 server+ and
to deploy a production quality Mobius project.

config.yaml
-----------

Settings used to generate files from the templates in the conf directory.

deviceproxy_site.yaml
---------------------

Configuration to be used by https://pypi.python.org/pypi/device-proxy. Required when a site serves
mobile and desktop devices on different subdomains.

handler.py
----------

Module containing logic to distunguish between basic, smart and web devices using information
supplied by device-proxy.

requirements.txt
----------------

Versions of products required for the project.

setup-development.sh
--------------------

Script to setup a development environment.

test_settings.py
----------------

Django settings for use in unit tests.

wsgi.py
-------

Script to run the site as a WSGI server.

