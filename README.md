# Hardware Info API

A lightweight Python-based API designed to run on any device, providing real-time monitoring of system metrics including CPU usage, temperature, RAM, and storage.

Can be used with a dedicated [web interface](https://github.com/michalges/raspberrypi-web-app).

## Used Technologies

- Python
- FastAPI
- DuckDB
- Docker

## Requirements

- Git
- Docker

## How to run

- clone repository:

    ```bash
    git clone https://github.com/michalges/hardware-info-api
    cd hardware-info-api
    ```

- run Docker container:

    ```bash
    docker build -t hardware-info-api .
    docker run -d -p 8080:8080 --name hardware-info-api hardware-info-api
    ```

## Endpoints

To view all available endpoints, run the app and visit [/docs](http://localhost:8080/docs)
