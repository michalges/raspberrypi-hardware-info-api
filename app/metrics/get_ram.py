import psutil
from app.utils import bytes_to_gb


def get_ram():
    try:
        return bytes_to_gb(psutil.virtual_memory().used)
    except:
        return None
