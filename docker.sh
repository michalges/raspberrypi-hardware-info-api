#!/bin/bash

docker compose build || exit 1
docker compose up -d