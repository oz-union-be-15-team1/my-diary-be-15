# app/main.py

from fastapi import FastAPI
# .core와 .db는 현재 패키지(app) 내에 있습니다.
from .core.config import settings
from .db.session import init_tortoise


# 1. FastAPI 애플리케이션 인스턴스 정의
app = FastAPI(
    title="My Diary API",
    description="FastAPI, Tortoise ORM, and PostgreSQL Backend",
    version="1.0.0",
)


# 2. 데이터베이스 연결 이벤트 등록
# 서버 시작 시 ORM 설정 및 DB 연결을 시도합니다.
init_tortoise(app)


# 3. 테스트용 루트 라우터
@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI Backend!", "db_url_status": "Loaded from .env"}