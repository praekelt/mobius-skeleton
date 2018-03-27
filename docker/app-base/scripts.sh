#!/bin/sh

# Run all scripts in the scripts directory in alphabetical order

if [ -d "/var/app/docker/app/scripts" ]; then
for FILE in $( ls /var/app/docker/app/scripts ); do
     exec "/var/app/docker/app/scripts/${FILE}"
done
fi
