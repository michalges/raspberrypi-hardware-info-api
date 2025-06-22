REVISION_MAP = {
    "a02082": "Raspberry Pi 3 Model B",
    "a22082": "Raspberry Pi 3 Model B",
    "900092": "Raspberry Pi Zero",
    "a020d3": "Raspberry Pi 3 Model B+",
    "a03111": "Raspberry Pi 4 Model B 1GB",
    "b03111": "Raspberry Pi 4 Model B 2GB",
    "c03111": "Raspberry Pi 4 Model B 4GB",
    "d03114": "Raspberry Pi 4 Model B 8GB",
    "d03114": "Raspberry Pi 4 Model B 8GB",
    "d04171": "Raspberry Pi 5 8GB",
}

def get_rpi_revision():
    try:
        with open("/proc/cpuinfo") as f:
            for line in f:
                if line.startswith("Revision"):
                    return line.strip().split(":")[1].strip()
    except Exception:
        return None


def get_device_info():        
    revision = get_rpi_revision()
    if revision is not None:
        model = REVISION_MAP.get(revision.lower(), "Unknown or unsupported Raspberry Pi model")
    else:
        model = "Unknown model"
    return {"revision": revision, "model": model}