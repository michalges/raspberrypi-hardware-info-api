def bytes_to_gb(bytes_val: int, precision: int = 2) -> float:
    return round(bytes_val / (1024**3), precision)
