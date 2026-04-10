from datetime import datetime
from sqlmodel import SQLModel, Field


class SystemMetrics(SQLModel, table=True):
    timestamp: datetime = Field(primary_key=True)
    cpu_usage: float | None = None
    temp: float | None = None
    ram_usage: float | None = None
    storage_usage: float | None = None
