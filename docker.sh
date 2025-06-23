#!/bin/bash

docker build -t raspberrypi-hardware-info-api . || exit 1
container_id=$(docker run -d --restart always -p 8080:8080 raspberrypi-hardware-info-api)
echo "Container ID: $container_id"
