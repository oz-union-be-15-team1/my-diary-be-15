from fastapi import APIRouter
from . import question 
from . import auth     # 💡 auth 라우터 임포트

api_router = APIRouter()

api_router.include_router(question.router)
api_router.include_router(auth.router)  # 💡 [필수] 이 한 줄이 문제의 핵심입니다.