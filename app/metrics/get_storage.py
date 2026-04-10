import psutil


def get_storage():
    try:
        return round(psutil.disk_usage("/").used / 1024**3, 2)
    except:
        return None
