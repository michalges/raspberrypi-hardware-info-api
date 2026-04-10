import psutil


def get_cpu():
    try:
        val = psutil.cpu_percent(interval=None)
        return round(val, 2) if val is not None else None
    except:
        return None
