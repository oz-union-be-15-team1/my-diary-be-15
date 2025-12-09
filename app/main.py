from fastapi import FastAPI
from app.db.session import init_tortoise
from app.api.v1 import auth as auth_router
from app.api.v1 import diary as diary_router

app = FastAPI(title="Daily Healing Log")

app.include_router(auth_router.router)
app.include_router(diary_router.router)

init_tortoise(app)
