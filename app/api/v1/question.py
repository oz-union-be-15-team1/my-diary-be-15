# app/api/v1/question.py

# FastAPI 핵심 모듈 임포트: 라우터 정의, 의존성 주입, 예외 처리
from fastapi import APIRouter, Depends, HTTPException
# 서비스 계층 임포트: 실제 비즈니스 로직(랜덤 질문 조회)을 수행합니다.
from app.services.question_service import QuestionService
# ORM 모델 임포트: 인증 의존성 함수가 반환할 사용자 객체의 타입 힌트로 사용됩니다.
from app.models.user import User
# Pydantic 스키마 임포트: 응답 데이터의 형식과 유효성을 정의합니다.
from app.schemas.question import Question_Pydantic
# 인증 의존성 함수 임포트: 요청 헤더의 JWT 토큰을 검증하고 사용자 객체를 가져옵니다.
from app.core.security import get_current_user

# 라우터 인스턴스 생성: 이 파일의 엔드포인트에 /questions 프리픽스와 태그를 할당합니다.
router = APIRouter(prefix="/questions", tags=["Questions"])

# GET /api/v1/questions/random 엔드포인트 정의
@router.get(
    "/random",
    # 응답 모델 정의: 이 함수가 성공적으로 반환할 JSON 데이터의 형식을 Question_Pydantic 스키마로 강제합니다.
    response_model=Question_Pydantic,
    summary="사용자에게 할당되지 않은 랜덤 질문 조회"
)
async def get_random_question(
        # 💡 의존성 주입 (Authentication):
        # 요청이 들어올 때마다 get_current_user 함수가 실행됩니다.
        # 1. 요청 헤더에서 Bearer Token(JWT)을 추출합니다.
        # 2. JWT를 디코딩하고 검증합니다.
        # 3. 토큰의 user_id를 사용하여 DB에서 User 객체를 조회합니다.
        # 4. 검증 실패 시: 401 Unauthorized 예외를 즉시 발생시켜 라우터 함수 진입을 막습니다.
        # 5. 검증 성공 시: 조회된 User 객체를 'user' 변수에 할당합니다.
        user: User = Depends(get_current_user)
):
    """인증된 사용자를 위한 랜덤 질문을 반환합니다."""

    # 1. 서비스 계층 호출 및 오류 처리
    try:
        # QuestionService로 제어를 넘겨 랜덤 질문 조회 비즈니스 로직을 실행합니다.
        # 이 함수는 Repository를 호출하여 DB에서 질문 모델 객체를 가져옵니다.
        question = await QuestionService.get_random_question()

    except Exception as e:
        # DB 연결 실패, 쿼리 오류 등 서비스 계층에서 발생한 모든 예상치 못한 오류를 잡습니다.
        print(f"Error fetching random question: {e}")
        # 클라이언트에게는 500 Internal Server Error를 반환합니다.
        raise HTTPException(status_code=500, detail="Failed to fetch question from service.")

    # 2. 질문 존재 여부 확인
    if not question:
        # QuestionService가 질문을 찾지 못하고 None을 반환한 경우 (예: DB에 질문 없음)
        # 클라이언트에게는 404 Not Found 예외를 반환합니다.
        raise HTTPException(status_code=404, detail="No questions found in database.")

    # 3. 응답 데이터 변환 및 반환
    # Tortoise ORM 모델 객체(question)를 Pydantic 스키마(Question_Pydantic)로 변환합니다.
    # 이 과정에서 DB에서 가져온 데이터가 응답 모델 형식과 일치하는지 검증됩니다.
    return await Question_Pydantic.from_tortoise_orm(question)