# app/services/question_service.py

from app.repositories.question_repo import QuestionRepository
from app.models.question import Question
from typing import Optional

class QuestionService:
    """
    질문 관련 비즈니스 로직을 처리합니다.
    """
    @staticmethod
    async def get_random_question_for_user(user_id: int) -> Optional[Question]:
        """
        사용자에게 할당되지 않은 랜덤 질문을 Repository를 통해 조회합니다.
        """
        return await QuestionRepository.get_random_unassigned_question(user_id)