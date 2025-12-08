# app/api/v1/question.py (수정)

from fastapi import APIRouter, Depends, HTTPException # HTTPException은 그대로 유지
from app.services.question_service import QuestionService
from app.models.user import User
from app.schemas.question import Question_Pydantic

# ❌ 다음 임포트 구문을 제거하거나 주석 처리합니다:
# from tortoise.contrib.fastapi import HTTPNotFoundError 


router = APIRouter(prefix="/questions", tags=["Questions"])

# API 정의 수정: responses={404: {"model": HTTPNotFoundError}} 부분을 제거합니다.
@router.get(
    "/random",
    response_model=Question_Pydantic,
    # 💡 404 응답 모델 명시를 삭제하거나, FastAPI 표준 스키마를 사용합니다.
    # responses={404: {"model": HTTPNotFoundError}}, <- 이 줄을 제거합니다.
    summary="사용자에게 할당되지 않은 랜덤 질문 조회"
)
async def get_random_question(
    # ... (함수 내용 동일)
):
    # ...
    if not question:
        # HTTPException을 사용하면 FastAPI가 자동으로 404 응답을 생성합니다.
        raise HTTPException(status_code=404, detail="모든 질문에 답변했거나 질문이 없습니다.")
        
    return await Question_Pydantic.from_tortoise_orm(question)