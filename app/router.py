from typing import Annotated

from fastapi import APIRouter, Depends
from sqlmodel import Session

from app import controller
from app.db.database import get_session

router = APIRouter(prefix="/api/v1")
metrics_router = APIRouter(prefix="/metrics", tags=["Metrics"])

SessionDep = Annotated[Session, Depends(get_session)]


@router.get("/")
def get_root():
    return {"name": "hardware-info-api"}


@router.get("/device")
def get_device_info():
    return controller.fetch_device_info()


@metrics_router.get("/all")
def get_current_metrics(session: SessionDep):
    return controller.fetch_all_metrics(session)


@metrics_router.get("/all/history")
def get_current_metrics_history(session: SessionDep):
    return controller.fetch_all_metrics_history(session)


@metrics_router.get("/cpu")
def get_cpu(session: SessionDep):
    return controller.fetch_cpu_info(session)


@metrics_router.get("/cpu/history")
def get_cpu_history(session: SessionDep):
    return controller.fetch_cpu_history(session)


@metrics_router.get("/temp")
def get_temp(session: SessionDep):
    return controller.fetch_temp_info(session)


@metrics_router.get("/temp/history")
def get_temp_history(session: SessionDep):
    return controller.fetch_temp_history(session)


@metrics_router.get("/ram")
def get_ram(session: SessionDep):
    return controller.fetch_ram_info(session)


@metrics_router.get("/ram/history")
def get_ram_history(session: SessionDep):
    return controller.fetch_ram_history(session)


@metrics_router.get("/storage")
def get_storage(session: SessionDep):
    return controller.fetch_storage_info(session)


@metrics_router.get("/storage/history")
def get_storage_history(session: SessionDep):
    return controller.fetch_storage_history(session)


router.include_router(metrics_router)
