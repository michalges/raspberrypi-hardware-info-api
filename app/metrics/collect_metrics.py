import time
from datetime import datetime, timedelta, timezone

from sqlalchemy import Engine
from sqlmodel import Session, col, delete
from app.db.models import SystemMetrics
from app.metrics.get_cpu import get_cpu
from app.metrics.get_temperature import get_temperature
from app.metrics.get_ram import get_ram
from app.metrics.get_storage import get_storage

RETENTION_PERIOD = timedelta(days=1)
FETCH_INTERVAL = 5


def collect_metrics(engine: Engine):
    while True:
        try:
            current_time = datetime.now(timezone.utc)
            cutoff_time = current_time - RETENTION_PERIOD

            new_metric = SystemMetrics(
                timestamp=current_time,
                cpu_usage=get_cpu(),
                temperature=get_temperature(),
                ram_usage=get_ram(),
                storage_usage=get_storage(),
            )
            with Session(engine) as session:
                statement = delete(SystemMetrics).where(
                    col(SystemMetrics.timestamp) < cutoff_time
                )
                session.exec(statement)
                session.add(new_metric)
                session.commit()
        except Exception as e:
            print(f"Error occurred while saving metrics: {e}")

        time.sleep(FETCH_INTERVAL)
