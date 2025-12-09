# app/repositories/question_repo.py

from app.models.question import Question
from typing import Optional

class QuestionRepository:
    """
    질문 데이터베이스 접근 및 쿼리 로직을 담당합니다.
    """
    @staticmethod
    async def get_random_unassigned_question(user_id: int) -> Optional[Question]:
        """
        특정 사용자(user_id)에게 할당되지 않은 질문 중 하나를 랜덤으로 조회합니다.
        """

        # 1. 사용자가 이미 답변했거나 할당받은 질문의 ID 목록을 가져옵니다.
        # (UserQuestion 모델의 related_name='assigned_questions'와 Question 모델의 related_name='assigned_users'를 사용)
        answered_question_ids = [
            uq.question_id
            async for uq in Question.assigned_users.all() if uq.user_id == user_id
        ]

        # 2. 이미 답변된 질문을 제외하고, 나머지 질문들을 랜덤으로 선택합니다.
        # .exclude()와 .order_by('?')를 사용하여 구현합니다.
        question = await Question.filter(
            id__not_in=answered_question_ids
        ).order_by('?')

        # 3. 결과 리스트가 비어있지 않다면 첫 번째 질문을 반환합니다.
        if question:
            return question[0]
        return None