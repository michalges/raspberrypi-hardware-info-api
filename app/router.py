from typing import Annotated

from fastapi import APIRouter, Depends
from sqlmodel import Session

from app import controller
from app.db.database import get_session

router = APIRouter()

SessionDep = Annotated[Session, Depends(get_session)]


@router.get("/")
def get_root():
    return {"name": "hardware-info-api"}


@router.get("/device")
def get_device_info():
    return controller.fetch_device_info()


@router.get("/current_metrics")
def get_current_metrics(session: SessionDep):
    return controller.fetch_current_metrics(session)


@router.get("/current_metrics/history")
def get_current_metrics_history(session: SessionDep):
    return controller.fetch_current_metrics_history(session)


@router.get("/cpu")
def get_cpu(session: SessionDep):
    return controller.fetch_cpu_info(session)


@router.get("/cpu/history")
def get_cpu_history(session: SessionDep):
    return controller.fetch_cpu_history(session)


@router.get("/temp")
def get_temp(session: SessionDep):
    return controller.fetch_temp_info(session)


@router.get("/temp/history")
def get_temp_history(session: SessionDep):
    return controller.fetch_temp_history(session)


@router.get("/ram")
def get_ram(session: SessionDep):
    return controller.fetch_ram_info(session)


@router.get("/ram/history")
def get_ram_history(session: SessionDep):
    return controller.fetch_ram_history(session)


@router.get("/storage")
def get_storage(session: SessionDep):
    return controller.fetch_storage_info(session)


@router.get("/storage/history")
def get_storage_history(session: SessionDep):
    return controller.fetch_storage_history(session)
