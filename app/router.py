from fastapi import APIRouter
from app.get_stats import cpu_usage_history, temp_history, ram_history, storage_history
from app.get_device_info import get_device

router = APIRouter()


@router.get("/")
def get_root():
    return {"name": "hardware-info-api"}


@router.get("/cpu")
def get_cpu():
    if cpu_usage_history:
        return max(cpu_usage_history, key=lambda x: x.get("timestamp", 0))
    return {}


@router.get("/cpu/history")
def get_cpu_history():
    return list(cpu_usage_history)


@router.get("/temp")
def get_temp():
    if temp_history:
        return max(temp_history, key=lambda x: x.get("timestamp", 0))
    return {}


@router.get("/temp/history")
def get_temp_history():
    return list(temp_history)


@router.get("/ram")
def get_ram():
    if ram_history:
        return max(ram_history, key=lambda x: x.get("timestamp", 0))
    return {}


@router.get("/ram/history")
def get_ram_history():
    return list(ram_history)


@router.get("/storage")
def get_storage():
    if storage_history:
        return max(storage_history, key=lambda x: x.get("timestamp", 0))
    return {}


@router.get("/storage/history")
def get_storage_history():
    return list(storage_history)


@router.get("/device")
def get_device_info():
    return get_device()


@router.get("/stats")
def system_stats():
    return {
        "cpu": get_cpu(),
        "temp": get_temp(),
        "ram": get_ram(),
        "storage": get_storage(),
    }
