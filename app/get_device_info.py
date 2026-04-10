import psutil


RPI_MODEL_NAMES = {
    "a02082": "Raspberry Pi 3 Model B",
    "a22082": "Raspberry Pi 3 Model B",
    "900092": "Raspberry Pi Zero",
    "a020d3": "Raspberry Pi 3 Model B+",
    "a03111": "Raspberry Pi 4 Model B 1GB",
    "b03111": "Raspberry Pi 4 Model B 2GB",
    "c03111": "Raspberry Pi 4 Model B 4GB",
    "d03114": "Raspberry Pi 4 Model B 8GB",
    "d04171": "Raspberry Pi 5 8GB",
}


def get_rpi_revision() -> str | None:
    """Attempts to read the Raspberry Pi model name."""
    try:
        with open("/proc/cpuinfo") as f:
            for line in f:
                if line.startswith("Revision"):
                    return RPI_MODEL_NAMES.get(
                        line.strip().split(":")[1].strip().lower(),
                        "Raspberry Pi (unknown model)",
                    )
    except Exception:
        return None


def get_device_model():
    # TODO: Add support for other devices
    device = get_rpi_revision()

    return device


def get_device_info():
    return {"device_name": get_device_model()}
