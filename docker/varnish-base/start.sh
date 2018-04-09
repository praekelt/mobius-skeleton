#!/bin/sh

python /src/django-ultracache/cache-purge-consumer.py -c /purge.yaml &
varnishd -F -f /etc/varnish/default.vcl
