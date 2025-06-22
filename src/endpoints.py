from fastapi import APIRouter
from src.stats import cpu_usage_history, temp_history, ram_history, storage_history
from src.get_device_info import get_device_info
import socket
import platform
import os
from typing import Dict, Any
import subprocess

router = APIRouter()

@router.get("/cpu")
def get_cpu_history():
    return list(cpu_usage_history)

@router.get("/temp")
def get_temp_history():
    return list(temp_history)

@router.get("/ram")
def get_ram_history():
    return list(ram_history)

@router.get("/storage")
def get_storage_history():
    return list(storage_history)

REVISION_MAP = {
    "a02082": "Raspberry Pi 3 Model B",
    "a22082": "Raspberry Pi 3 Model B",
    "900092": "Raspberry Pi Zero",
    "a020d3": "Raspberry Pi 3 Model B+",
    "a03111": "Raspberry Pi 4 Model B 1GB",
    "b03111": "Raspberry Pi 4 Model B 2GB",
    "c03111": "Raspberry Pi 4 Model B 4GB",
    "d03114": "Raspberry Pi 4 Model B 8GB",
    "d03114": "Raspberry Pi 4 Model B 8GB",
    "d04171": "Raspberry Pi 5 8GB",
}

def get_rpi_revision():
    try:
        with open("/proc/cpuinfo") as f:
            for line in f:
                if line.startswith("Revision"):
                    return line.strip().split(":")[1].strip()
    except Exception:
        return None

@router.get("/device")
def device():
    return get_device_info()