import psutil


def get_temp() -> float | None:
    """
    Attempts to get the CPU temperature in Celsius across different operating systems.
    """

    if psutil and hasattr(psutil, "sensors_temperatures"):
        try:
            temps = psutil.sensors_temperatures()
            if temps:
                for name in ["coretemp", "k10temp", "cpu_thermal", "cpu-thermal"]:
                    if name in temps and temps[name]:
                        return temps[name][0].current
                return list(temps.values())[0][0].current
        except Exception:
            pass

    try:
        with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
            return int(f.read().strip()) / 1000.0
    except Exception:
        pass

    # TODO: MacOS and WSL support

    return None
