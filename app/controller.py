from collections.abc import Sequence
from datetime import datetime
from typing import Any
from sqlmodel import Session, asc, desc, select, text

from app.db.models import SystemMetrics
from app.get_device_info import get_device_info
from app.system_info import get_device_ram_info, get_device_storage_info

device_info = get_device_info()
device_ram_info = get_device_ram_info()
device_storage_info = get_device_storage_info()


def _get_latest_record(session: Session) -> SystemMetrics | None:
    return session.exec(
        select(SystemMetrics).order_by(desc(SystemMetrics.timestamp))
    ).first()


def _get_metric_history_raw(
    session: Session, metric_column: Any
) -> Sequence[tuple[Any, datetime]]:
    return session.exec(
        select(metric_column, SystemMetrics.timestamp).order_by(
            asc(SystemMetrics.timestamp)
        )
    ).all()


def _fetch_detailed_history_generic(
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


def _format_metric_response(
    record: SystemMetrics | None, field_name: str, extra: dict[str, Any] | None = None
):
    data: dict[str, Any] = {
        field_name: getattr(record, field_name, None) if record else None,
        "timestamp": getattr(record, "timestamp", None) if record else None,
    }
    if extra:
        data.update(extra)
    return data


def _format_history_response(
    records: Sequence[tuple[Any, datetime]],
    field_name: str,
    extra: dict[str, Any] | None = None,
):
    data: dict[str, Any] = {
        "records": [{field_name: val, "timestamp": ts} for val, ts in records]
    }
    if extra:
        data["info"] = extra
    return data


def fetch_device_info():
    return device_info


def fetch_all_metrics(session: Session):
    record = _get_latest_record(session)
    if not record:
        return {**device_ram_info, **device_storage_info}
    return {
        **record.model_dump(),
        **device_ram_info,
        **device_storage_info,
    }


def fetch_all_metrics_history(session: Session):
    return {
        "info": {**device_ram_info, **device_storage_info},
        "data": session.exec(
            select(SystemMetrics).order_by(desc(SystemMetrics.timestamp))
        ).all(),
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
            round(AVG(temperature), 2) as avg_temp,
            round(MIN(temperature), 2) as min_temp,
            round(MAX(temperature), 2) as max_temp,
            round(AVG(ram_usage), 2) as avg_ram,
            round(MIN(ram_usage), 2) as min_ram,
            round(MAX(ram_usage), 2) as max_ram,
            round(AVG(storage_usage), 2) as avg_storage,
            round(MIN(storage_usage), 2) as min_storage,
            round(MAX(storage_usage), 2) as max_storage
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


def fetch_cpu_info(session: Session):
    return _format_metric_response(_get_latest_record(session), "cpu_usage")


def fetch_cpu_history(session: Session):
    return _format_history_response(
        _get_metric_history_raw(session, SystemMetrics.cpu_usage), "cpu_usage"
    )


def fetch_cpu_detailed_history(session: Session, interval: str = "1 minute"):
    return {"records": _fetch_detailed_history_generic(session, "cpu_usage", interval)}


def fetch_temperature_info(session: Session):
    return _format_metric_response(_get_latest_record(session), "temperature")


def fetch_temperature_history(session: Session):
    return _format_history_response(
        _get_metric_history_raw(session, SystemMetrics.temperature), "temperature"
    )


def fetch_temperature_detailed_history(session: Session, interval: str = "1 minute"):
    return {
        "records": _fetch_detailed_history_generic(session, "temperature", interval)
    }


def fetch_ram_info(session: Session):
    return _format_metric_response(
        _get_latest_record(session), "ram_usage", device_ram_info
    )


def fetch_ram_history(session: Session):
    return _format_history_response(
        _get_metric_history_raw(session, SystemMetrics.ram_usage),
        "ram_usage",
        device_ram_info,
    )


def fetch_ram_detailed_history(session: Session, interval: str = "1 minute"):
    return {
        "info": device_ram_info,
        "records": _fetch_detailed_history_generic(session, "ram_usage", interval),
    }


def fetch_storage_info(session: Session):
    return _format_metric_response(
        _get_latest_record(session), "storage_usage", device_storage_info
    )


def fetch_storage_history(session: Session):
    return _format_history_response(
        _get_metric_history_raw(session, SystemMetrics.storage_usage),
        "storage_usage",
        device_storage_info,
    )


def fetch_storage_detailed_history(session: Session, interval: str = "1 minute"):
    return {
        "info": device_storage_info,
        "records": _fetch_detailed_history_generic(session, "storage_usage", interval),
    }
