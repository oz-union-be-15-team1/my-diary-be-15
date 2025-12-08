# app/api/v1/__init__.py (예상)

from fastapi import APIRouter
from . import question # 💡 새로 추가된 question 라우터 임포트

# from . import auth, diary, quote, bookmark # 다른 라우터도 임포트되어야 합니다.

api_router = APIRouter()

# 랜덤 질문 API 포함
api_router.include_router(question.router)
# 다른 라우터들도 여기에 포함되어야 합니다.
# api_router.include_router(auth.router, prefix="/auth") 
# api_router.include_router(diary.router, prefix="/diaries") 
# ...