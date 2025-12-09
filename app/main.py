# app/main.py (최종 정리 버전)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.v1 import api_router
from .db.session import init_tortoise # DB 초기화 함수 임포트

# 1. FastAPI 앱 인스턴스 생성 (키워드 인수 사용)
app = FastAPI(
    title="My Diary API", 
    version="1.0.0", 
    docs_url="/docs",
    redoc_url=None
)

# 2. CORS 미들웨어 등록
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. 💡 Tortoise ORM 초기화 호출 (미들웨어 후, 라우터 등록 전에 위치)
# 이 호출은 @app.on_event("startup")에 DB 연결 로직을 등록합니다.
init_tortoise(app) 

# 4. 라우터 등록 (항상 마지막에)
app.include_router(api_router, prefix="/api/v1")