#!/bin/bash

git pull
docker build -t simpletabs:latest .
docker stop $(docker ps -q --filter ancestor=simpletabs)
docker system prune -f
docker run -d -p 0.0.0.0:5000:5000 simpletabs
