from collections.abc import Sequence
from datetime import datetime
from typing import Any
from sqlmodel import Session, asc, desc, select, text

import psutil

from app.db.models import SystemMetrics
from app.get_device_info import get_device_info
from app.utils import bytes_to_gb


def get_device_ram_info():
    try:
        mem = psutil.virtual_memory()
        return {
            "ram_total": bytes_to_gb(mem.total),
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
            "storage_total": bytes_to_gb(disk.total),
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


def fetch_metric_detailed_history(
    session: Session, column_name: str, interval: str = "1 minute"
):
    table_name = SystemMetrics.__tablename__
    query = text(
        f"""
        SELECT
            time_bucket(CAST(:interval AS INTERVAL), timestamp) AS bucket_start,
            round(AVG({column_name}), 2) as avg_val,
            round(MIN({column_name}), 2) as min_val,
            round(MAX({column_name}), 2) as max_val
        FROM {table_name}
        GROUP BY bucket_start
        ORDER BY bucket_start ASC
    """
    )
    results = session.execute(query, {"interval": interval}).all()
    return [
        {
            "timestamp": r[0],
            "avg": r[1],
            "min": r[2],
            "max": r[3],
        }
        for r in results
    ]


def fetch_device_info():
    return device_info


def fetch_all_metrics(session: Session):
    record = get_latest_record(session)

    if not record:
        return {
            **device_ram_info,
            **device_storage_info,
        }

    return {
        **record.model_dump(),
        **device_ram_info,
        **device_storage_info,
    }


def fetch_detailed_history(session: Session, interval: str = "1 minute"):
    table_name = SystemMetrics.__tablename__
    query = text(
        f"""
        SELECT
            time_bucket(CAST(:interval AS INTERVAL), timestamp) AS bucket_start,
            round(AVG(cpu_usage), 2) as avg_cpu,
            round(MIN(cpu_usage), 2) as min_cpu,
            round(MAX(cpu_usage), 2) as max_cpu,
            round(AVG(temperature), 2) as avg_temperature,
            round(MIN(temperature), 2) as min_temperature,
            round(MAX(temperature), 2) as max_temperature,
            round(AVG(ram_usage), 2) as avg_ram,
            round(MIN(ram_usage), 2) as min_ram,
            round(MAX(ram_usage), 2) as max_ram,
            round(AVG(storage_usage), 2) as avg_storage,
            round(MIN(storage_usage), 2) as min_storage,
            round(MAX(storage_usage), 2) as max_storage,
        FROM {table_name}
        GROUP BY bucket_start
        ORDER BY bucket_start ASC
    """
    )
    results = session.execute(query, {"interval": interval}).all()

    return [
        {
            "timestamp": r[0],
            "cpu": {"avg": r[1], "min": r[2], "max": r[3]},
            "temperature": {"avg": r[4], "min": r[5], "max": r[6]},
            "ram": {"avg": r[7], "min": r[8], "max": r[9]},
            "storage": {"avg": r[10], "min": r[11], "max": r[12]},
        }
        for r in results
    ]


def fetch_all_metrics_history(session: Session):
    return {
        "info": {
            **device_ram_info,
            **device_storage_info,
        },
        "data": session.exec(
            select(SystemMetrics).order_by(desc(SystemMetrics.timestamp))
        ).all(),
    }


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


def fetch_cpu_detailed_history(session: Session, interval: str = "1 minute"):
    return {
        "records": fetch_metric_detailed_history(session, "cpu_usage", interval),
    }


def fetch_temperature_info(session: Session):
    record = get_latest_record(session)
    return (
        {"temperature": record.temperature, "timestamp": record.timestamp}
        if record
        else {"temperature": None, "timestamp": None}
    )


def fetch_temperature_history(session: Session):
    records = get_metric_history(session, SystemMetrics.temperature)
    return {"records": [{"temperature": val, "timestamp": ts} for val, ts in records]}


def fetch_temperature_detailed_history(session: Session, interval: str = "1 minute"):
    return {
        "records": fetch_metric_detailed_history(session, "temperature", interval),
    }


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


def fetch_ram_detailed_history(session: Session, interval: str = "1 minute"):
    return {
        "info": device_ram_info,
        "records": fetch_metric_detailed_history(session, "ram_usage", interval),
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


def fetch_storage_detailed_history(session: Session, interval: str = "1 minute"):
    return {
        "info": device_storage_info,
        "records": fetch_metric_detailed_history(session, "storage_usage", interval),
    }
