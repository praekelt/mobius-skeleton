#!/bin/sh

python /src/django-ultracache-twisted/purge/threaded.py -c /purge.yaml &
varnishd -F -f /etc/varnish/default.vcl
