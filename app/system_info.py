import psutil
from app.get_device_info import get_device_info
from app.utils import bytes_to_gb


def get_device_ram_info():
    try:
        mem = psutil.virtual_memory()
        return {
            "ram_total": bytes_to_gb(mem.total),
            "ram_unit": "GB",
        }
    except:
        return {
            "ram_total": None,
            "ram_unit": "GB",
        }


def get_device_storage_info():
    try:
        disk = psutil.disk_usage("/")
        return {
            "storage_total": bytes_to_gb(disk.total),
            "storage_unit": "GB",
        }
    except:
        return {
            "storage_total": None,
            "storage_unit": "GB",
        }
