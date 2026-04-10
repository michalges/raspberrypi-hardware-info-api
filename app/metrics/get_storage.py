import psutil
from app.utils import bytes_to_gb


def get_storage():
    try:
        return bytes_to_gb(psutil.disk_usage("/").used)
    except:
        return None
