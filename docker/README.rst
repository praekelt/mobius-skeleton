Mobius Docker
=============

Overview
--------

The purpose of this directory is to bootstrap a complete Docker setup for
Mobius projects through Docker Compose. The design goal is to have all Docker
related files living in one directory tree, thus avoiding pollution.
Unfortunately the .dockerignore currently requires a fixed location in the repo
root and causes slight pollution.

Topology
--------

Todo.

Preparing your environment
--------------------------

If your Mobius project does not already have this directory then copy it
across. You may want to periodically re-synch this directory with the
latest version in mobius-skeleton.

Ensure you have the latest version ob mobius installed. It provides the
``create_admin_user`` management command.

Both Docker and Docker Compose must be installed.

Nginx
*****

``nginx-base`` provides a reasonable ``nginx.template``. If it is not sufficient then
create ``nginx/nginx.template`` and provide your own version.

Varnish
*******

Django Cache Headers generates a VCL declaration that describes the
reverse caching rules. From your Django app's root directory on your development
instance do::

    python manage.py generate_vcl > vclhash.vcl

Place this file in ``varnish/vclhash.vcl``.

App
***

Your Mobius-based app's source code lives in ``app/``. Modify ``app/Dockerfile``
if you have any extra build commands.

The daphne, runworker, celery worker and celery beat images all inherit
from this app image.

If you need to run arbitrary commands after database migration then place
shell scripts in ``app/scripts/``. The shell scripts are executed in
alphabetical order.

Running it
----------

This assumes you have both docker and docker-compose installed::

    ./docker-compose myproject

or, if your OS users are set up differently::

    sudo ./docker-compose myproject

Navigate to http://192.168.17.10 or https://192.168.17.11 in your browser.

Admin::

    #. https://192.168.17.10/admin/. Login with ``admin``, ``local``.

Initiate a websocket chat by opening ``ws://nginx/ws/echo``. ``wscat`` is
a useful command line tool::

    wscat -c ws://192.168.17.10/ws/echo

Initiate a secure websocket with::

    wscat -n -c wss://192.168.17.10/ws/echo

