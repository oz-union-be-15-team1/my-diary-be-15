# app/api/v1/__init__.py

from fastapi import APIRouter

# 1. 하위 라우터 임포트 (하나씩 주석 해제)
from . import auth # 먼저 이 줄을 해제하고 서버가 재시작되는지 확인
# from . import diary
# from . import question
# from . import user

api_router = APIRouter()

# 2. 라우터 포함 (해제한 임포트에 맞춰 하나씩 추가)
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
# api_router.include_router(diary.router, prefix="/diary", tags=["diary"])
# .