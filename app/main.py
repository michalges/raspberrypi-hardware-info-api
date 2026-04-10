from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.router import router
from app.metrics.collect_metrics import collect_metrics
import threading
from contextlib import asynccontextmanager
from sqlmodel import SQLModel

from app.db.models import SystemMetrics  # type: ignore
from app.db.database import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)

    thread = threading.Thread(target=collect_metrics, args=(engine,), daemon=True)
    thread.start()

    yield


app = FastAPI(lifespan=lifespan)

app.include_router(router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
