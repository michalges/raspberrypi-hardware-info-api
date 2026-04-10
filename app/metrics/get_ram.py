import psutil


def get_ram():
    try:
        return round(psutil.virtual_memory().used / 1024**3, 2)
    except:
        return None
