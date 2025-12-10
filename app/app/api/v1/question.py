#app\api\v1\question.py
from fastapi import APIRouter, Depends, HTTPException
from app.services.question_service import get_random_question
# from app.core.security import get_current_user  # 향후 인증 적용 시 사용

# ------------------------------------------------------------
# APIRouter 설정
# ------------------------------------------------------------
# - FastAPI 라우터 그룹을 생성하는 역할.
# - tags=["Questions"] 는 Swagger UI에서 질문 API 그룹 이름을 의미함.
# - prefix는 main.py에서 "/api/v1/questions"로 이미 설정되어 있으므로,
#   여기서는 prefix를 다시 지정하지 않고 엔드포인트만 작성한다.
# ------------------------------------------------------------
router = APIRouter(tags=["Questions"])


# ============================================================
# 랜덤 자기성찰 질문 제공 API
# ------------------------------------------------------------
# [HTTP 메서드]  GET
# [엔드포인트]   /random
#
# [최종 URL]
#   main.py에서:
#       include_router(question_router, prefix="/api/v1/questions")
#   → 최종 엔드포인트 URL:
#       /api/v1/questions/random
#
# [역할]
#   - 서비스 레이어의 get_random_question()을 호출하여
#     데이터베이스에서 임의의 질문을 1개 가져와 사용자에게 반환.
#
# [구조]
#   클라이언트 → Router(여기) → Service(question_service) → Model(DB)
#
# [인증]
#   - 현재는 인증 필요 없음.
#   - 추후 필요하면 Depends(get_current_user)를 삽입하면 된다.
# ============================================================
@router.get("/random")
async def random_question_api():
    """
    랜덤 자기성찰 질문을 반환하는 API 엔드포인트.

    Returns (JSON):
        {
            "id": <질문 ID>,
            "question": <질문 내용>
        }

    Raises:
        HTTPException 404: 질문이 DB에 존재하지 않거나 비어있을 경우.
    """

    # ------------------------------------------------------------
    # [1] 서비스 레이어 호출
    # ------------------------------------------------------------
    # - 비즈니스 로직은 router가 아니라 "service"에서 처리한다.
    # - get_random_question() 함수는 DB에서 랜덤 질문 1개를 반환하거나,
    #   없으면 None을 반환한다.
    # - await 사용: 비동기(async) 환경이므로 반드시 await로 호출해야 함.
    # ------------------------------------------------------------
    question = await get_random_question()

    # ------------------------------------------------------------
    # [2] 결과 검증
    # ------------------------------------------------------------
    # 만약 DB에서 질문을 찾지 못하거나, 테이블이 비어있다면
    # question_service는 None을 반환하기 때문에 404 에러를 발생시킨다.
    # FastAPI의 HTTPException을 사용하면 자동으로
    # JSON 형태의 에러 응답과 상태 코드를 만들어준다.
    # ------------------------------------------------------------
    if not question:
        raise HTTPException(status_code=404, detail="질문 없음")

    # ------------------------------------------------------------
    # [3] 정상 응답 반환
    # ------------------------------------------------------------
    # - FastAPI는 딕셔너리를 반환하면 자동으로 JSON Response로 변환한다.
    # - question 객체는 Tortoise ORM 모델 객체이므로,
    #   필요한 필드만 사전(dict) 형태로 추출하여 반환한다.
    # ------------------------------------------------------------
    return {
        "id": question.id,
        "question": question.question_text
    }
