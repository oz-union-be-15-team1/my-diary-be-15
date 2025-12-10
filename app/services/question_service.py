# app/services/question_service.py

from app.repositories.question_repo import QuestionRepository
from app.models.question import Question
from typing import Optional
from tortoise.expressions import RawSQL

class QuestionService:
    # ============================================================
    # get_random_question()
    # ------------------------------------------------------------
    # [역할]
    #   - 데이터베이스에 저장된 자기성찰 질문(questions 테이블) 중
    #     "임의(Random)"로 1개 레코드를 선택하여 반환하는 서비스 로직.
    #
    # [구조적 위치]
    #   - Controller(API) → Service(여기) → Repository(optional) → Model(DB)
    #   - 즉, 서비스 계층은 "비즈니스 로직"만 담당하며,
    #     가능한 한 API(Route)와 DB Model을 분리하는 것이 목적.
    #
    # [사용 DB 함수]
    #   - PostgreSQL의 RANDOM() : 0~1 사이 난수를 생성하는 내장 함수
    #   - ORDER BY RANDOM()     : 각 레코드마다 난수를 부여한 뒤 정렬
    #   - LIMIT 1               : 정렬된 결과 중 첫 번째 한 개만 선택
    #
    # [Tortoise ORM .raw() 동작 방식]
    #   - ORM이 아니라 SQL을 직접 실행하는 Raw SQL Query 기능
    #   - Question.raw("SQL문") 은 모델 Question 객체 리스트로 결과 반환
    #
    # [반환 형태]
    #   - 레코드가 존재하면 Question 객체 반환
    #   - 비어 있으면 None 반환 (API에서는 404 처리 가능)
    # ============================================================
    @staticmethod
    async def get_random() -> Optional[Question]:
        # ------------------------------------------------------------
        # 1) SQL 직접 실행(RawSQL 사용)
        #    - ORM 방식이 아닌 직접 SQL 문장을 실행하여 데이터를 가져온다.
        #    - PostgreSQL RANDOM()을 사용하여, 모든 질문에 난수를 부여한 뒤,
        #      난수 기준으로 섞어서 맨 위의 한 개만 가져온다.
        #
        #    SQL:
        #       SELECT *
        #       FROM questions
        #       ORDER BY RANDOM()
        #       LIMIT 1;
        #
        # 2) Question.raw() 의 반환 타입
        #    - List[Question] 형태 (0개 또는 1개 이상의 Question 객체)
        #
        # 3) result[0] 으로 꺼내는 이유
        #    - LIMIT 1이므로 최대 1개만 존재
        # ------------------------------------------------------------
        result = await Question.raw(
            "SELECT * FROM question ORDER BY RANDOM() LIMIT 1;"
        )

        # ------------------------------------------------------------
        # 4) 만약 데이터가 존재하면 첫 번째 객체 반환
        #    - RawSQL Query 결과는 리스트 형태로 전달된다.
        # ------------------------------------------------------------
        if result:
            return result[0]

        # ------------------------------------------------------------
        # 5) 데이터가 없으면 None 반환
        #    - 서비스 계층에서는 None을 반환하도록 두고,
        #      API 계층에서 이를 보고 404 응답 등 처리 가능
        # ------------------------------------------------------------
        return None
