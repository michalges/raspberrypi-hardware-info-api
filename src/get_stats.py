import psutil, time
from collections import deque
from datetime import datetime, timezone
from src.config import FETCH_INTERVAL

cpu_usage_history = deque(maxlen=100)
temp_history = deque(maxlen=100)
ram_history = deque(maxlen=100)
storage_history = deque(maxlen=100)


def get_cpu_usage():
    try:
        return psutil.cpu_percent(interval=None)
    except:
        return None


def get_temp():
    try:
        with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
            return int(f.read().strip()) / 1000
    except:
        return None


def get_ram():
    try:
        mem = psutil.virtual_memory()
        return {
            "ram_used": round(mem.used / 1024**2, 2),
            "ram_total": round(mem.total / 1024**2, 2),
            "ram_available": round(mem.available / 1024**2, 2),
            "ram_percent_used": mem.percent,
            "ram_unit": "MB",
        }
    except:
        return None


def get_storage():
    try:
        disk = psutil.disk_usage("/")
        return {
            "storage_used": round(disk.used / 1024**3, 2),
            "storage_total": round(disk.total / 1024**3, 2),
            "storage_available": round(disk.free / 1024**3, 2),
            "storage_percent_used": disk.percent,
            "storage_unit": "GB",
        }
    except:
        return None


def collect_stats():
    while True:
        timestamp = datetime.now(timezone.utc).timestamp()

        cpu_usage = get_cpu_usage()
        temp = get_temp()
        ram = get_ram()
        storage = get_storage()

        if cpu_usage is not None:
            cpu_usage_history.append({"timestamp": timestamp, "cpu_usage": cpu_usage})

        if temp is not None:
            temp_history.append({"timestamp": timestamp, "temp": temp})

        if ram is not None:
            ram_flat = {"timestamp": timestamp}
            ram_flat.update(ram)
            ram_history.append(ram_flat)

        if storage is not None:
            storage_flat = {"timestamp": timestamp}
            storage_flat.update(storage)
            storage_history.append(storage_flat)

        time.sleep(FETCH_INTERVAL)
