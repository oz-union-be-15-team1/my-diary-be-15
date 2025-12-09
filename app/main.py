# app/main.py
from fastapi import FastAPI
from app.db.session import init_tortoise
from app.core.config import settings
from app.api.v1 import auth as auth_router
from app.api.v1 import diary as diary_router


app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG,
)

app.include_router(auth_router.router)
app.include_router(diary_router.router)

init_tortoise(app)

@app.get("/", summary="DB 연결 헬스 체크")
async def health_check():
    """
    서버 상태 확인용 루트 엔드포인트
    """
    return {"status": "healthy", "message": "OK"}
