#!/bin/bash

if [ $# -eq 0 ]
then
    echo "Usage: docker-compose.sh [projectname]"
    exit 1;
fi

echo "Once the containers are running you may browse to http://192.168.17.10"
read -n1 -r -p "Press any key to continue..." key

export PROJECT="$1"

# Build the base images
cd nginx-base
docker build -t praekeltcom/mobius-nginx-base:latest .
cd ../varnish-base
docker build -t praekeltcom/mobius-varnish-base:latest .
cd ../app-base
docker build -t praekeltcom/mobius-app-base:latest .

# Build the project images
cd ../nginx
docker build -t praekeltcom/mobius-nginx-${PROJECT}:latest .
cd ../varnish
docker build -t praekeltcom/mobius-varnish-${PROJECT}:latest .
cd ../..
docker build -f docker/app/Dockerfile -t praekeltcom/mobius-app-${PROJECT}:latest .
cd docker

docker-compose -f docker-compose.yml up
docker-compose -f docker-compose.yml down
