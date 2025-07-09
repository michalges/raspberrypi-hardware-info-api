# Raspberry Pi hardware info API

A lightweight Python-based API designed to run on your Raspberry Pi, providing real-time monitoring of system metrics including CPU usage, temperature, RAM, and storage.

API was made to work with [web interface](https://github.com/michalges/raspberrypi-web-app)

## Used Technologies

- Python
- FastAPI
- Docker

## Requirements

- Any Raspberry Pi model
- Docker and Git installed on the Raspberry Pi

## How to run

- clone repository:

    ```bash
    git clone https://github.com/michalges/raspberrypi-hardware-info-api
    cd raspberrypi-hardware-info-api
    ```

- run docker script:

    ```bash
    ./docker.sh
    ```

    This script starts the app and also ensures it will automatically restart and keep running on each boot.

- open [http://localhost:8080](http://localhost:8080) to see the app running

## Endpoints

To view all available endpoints, run the app and visit [/docs](http://localhost:8080/docs)
