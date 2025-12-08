from fastapi import FastAPI
from app.core.database import init_db

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    await init_db()
