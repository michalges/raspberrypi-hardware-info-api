# uvicorn src.main:app --host 0.0.0.0 --port 8080 --reload
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.endpoints import router
from src.stats import collect_stats
import threading
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    threading.Thread(target=collect_stats, daemon=True).start()
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

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}
