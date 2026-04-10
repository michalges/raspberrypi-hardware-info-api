import psutil


def get_cpu():
    try:
        return psutil.cpu_percent(interval=None)
    except:
        return None
