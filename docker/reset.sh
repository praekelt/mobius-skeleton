#!/bin/bash

# Remove all running containers
sudo docker rm -f `sudo docker ps -aq --no-trunc`

# Remove all mobius images
LINES=`sudo docker images | grep "mobius"`
if [ ! -z "$LINES" ]
then
    while read -r line; do
        sudo docker rmi -f `echo $line | awk '{print $3}'`
    done <<< "$LINES"
fi

# Remove all <none> images
LINES=`sudo docker images | grep "\<none\>"`
if [ ! -z "$LINES" ]
then
    while read -r line; do
        sudo docker rmi -f `echo $line | awk '{print $3}'`
    done <<< "$LINES"
fi
