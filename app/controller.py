from collections.abc import Sequence
from datetime import datetime
from typing import Any
from sqlmodel import Session, asc, desc, select

import psutil

from app.db.models import SystemMetrics
from app.get_device_info import get_device_info


def get_device_ram_info():
    try:
        mem = psutil.virtual_memory()
        return {
            "ram_total": round(mem.total / 1024**3, 2),
            "ram_unit": "GB",
        }
    except:
        return {
            "ram_total": None,
            "ram_unit": "GB",
        }


def get_device_storage_info():
    try:
        disk = psutil.disk_usage("/")
        return {
            "storage_total": round(disk.total / 1024**3, 2),
            "storage_unit": "GB",
        }
    except:
        return {
            "storage_total": None,
            "storage_unit": "GB",
        }


device_info = get_device_info()
device_ram_info = get_device_ram_info()
device_storage_info = get_device_storage_info()


def get_latest_record(session: Session) -> SystemMetrics | None:
    """Fetches a single, most recent SystemMetrics record."""
    return session.exec(
        select(SystemMetrics).order_by(desc(SystemMetrics.timestamp))
    ).first()


def get_metric_history(
    session: Session, metric_column: Any
) -> Sequence[tuple[Any, datetime]]:
    """Fetches historical data for a specific metric column."""
    return session.exec(
        select(metric_column, SystemMetrics.timestamp).order_by(
            asc(SystemMetrics.timestamp)
        )
    ).all()


def fetch_device_info():
    return device_info


def fetch_current_metrics(session: Session):
    return get_latest_record(session)


def fetch_current_metrics_history(session: Session):
    return session.exec(
        select(SystemMetrics).order_by(desc(SystemMetrics.timestamp))
    ).all()


def fetch_cpu_info(session: Session):
    record = get_latest_record(session)
    return (
        {"cpu_usage": record.cpu_usage, "timestamp": record.timestamp}
        if record
        else {"cpu_usage": None, "timestamp": None}
    )


def fetch_cpu_history(session: Session):
    records = get_metric_history(session, SystemMetrics.cpu_usage)
    return {"records": [{"cpu_usage": val, "timestamp": ts} for val, ts in records]}


def fetch_temp_info(session: Session):
    record = get_latest_record(session)
    return (
        {"temperature": record.temp, "timestamp": record.timestamp}
        if record
        else {"temperature": None, "timestamp": None}
    )


def fetch_temp_history(session: Session):
    records = get_metric_history(session, SystemMetrics.temp)
    return {"records": [{"temp": val, "timestamp": ts} for val, ts in records]}


def fetch_ram_info(session: Session):
    record = get_latest_record(session)
    return {
        "ram_usage": getattr(record, "ram_usage", None),
        "timestamp": getattr(record, "timestamp", None),
        **device_ram_info,
    }


def fetch_ram_history(session: Session):
    records = get_metric_history(session, SystemMetrics.ram_usage)
    return {
        "info": device_ram_info,
        "records": [{"ram_usage": val, "timestamp": ts} for val, ts in records],
    }


def fetch_storage_info(session: Session):
    record = get_latest_record(session)

    return {
        "storage_usage": getattr(record, "storage_usage", None),
        "timestamp": getattr(record, "timestamp", None),
        **device_storage_info,
    }


def fetch_storage_history(session: Session):
    records = get_metric_history(session, SystemMetrics.storage_usage)
    return {
        "info": device_storage_info,
        "records": [{"storage_usage": val, "timestamp": ts} for val, ts in records],
    }
