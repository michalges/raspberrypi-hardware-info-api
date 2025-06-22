# uvicorn src.main:app --host 0.0.0.0 --port 8080 --reload
from fastapi import FastAPI
from src.endpoints import router
from src.stats import collect_stats
import threading

app = FastAPI()

app.include_router(router)

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.on_event("startup")
def start_background_task():
    threading.Thread(target=collect_stats, daemon=True).start()
