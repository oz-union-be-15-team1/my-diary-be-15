# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db.session import init_tortoise
from app.core.config import settings
from app.api.v1 import auth as auth_router
from app.api.v1 import diary as diary_router
from app.api.v1 import quote as quote_router
from app.api.v1 import question as question_router

app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG,
)

# CORS 미들웨어 등록
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Tortoise ORM 초기화 호출 (미들웨어 후, 라우터 등록 전에 위치)
# 이 호출은 @app.on_event("startup")에 DB 연결 로직을 등록함
init_tortoise(app)

# 라우터 등록 (항상 마지막에)
app.include_router(auth_router.router)
app.include_router(diary_router.router)
app.include_router(quote_router.router)
app.include_router(question_router.router)



@app.get("/", summary="DB 연결 헬스 체크")
async def health_check():
    """
    서버 상태 확인용 루트 엔드포인트
    """
    return {"status": "healthy", "message": "OK"}
