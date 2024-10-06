#!/bin/bash

# get enviroment variables
source conf/config
 
# create images, containers and start them
docker compose up & # --no-cache

# list images and containers
docker ps -a
docker images

