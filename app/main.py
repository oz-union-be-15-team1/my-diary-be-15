# app/main.py

from fastapi import FastAPI
# 설정 파일 및 DB 세션 초기화 함수 임포트
from .core.config import settings
from .db.session import init_tortoise
from .api.v1 import api_router  # 💡 [필수] v1 API의 최상위 라우터 임포트


# 1. FastAPI 애플리케이션 인스턴스 정의
app = FastAPI(
    title="My Diary API",
    description="FastAPI, Tortoise ORM, and PostgreSQL Backend",
    version="1.0.0",
)


# 2. 데이터베이스 연결 이벤트 등록
# 서버 시작 시 ORM 설정 및 DB 연결을 시도합니다.
init_tortoise(app)


# 3. API 라우터 등록 [필수 추가]
# app/api/v1/__init__.py에 등록된 모든 라우터를 /api/v1 프리픽스로 등록합니다.
app.include_router(api_router, prefix="/api/v1")


# 4. 테스트용 루트 라우터 (기존 코드)
@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI Backend!", "db_url_status": "Loaded from .env"}