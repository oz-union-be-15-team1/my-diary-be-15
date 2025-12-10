#app\models\question.py
from tortoise import fields, models                                       # [1] Tortoise ORM 모델/필드 import


# =====================================================================
#  QUESTION MODEL  (질문 테이블)
# =====================================================================
class Question(models.Model):                                             # [2] 단일 질문 레코드
    """
    QUESTIONS 테이블
    - question_text만 가진 단순한 질문 테이블
    - UserQuestion 중간 테이블과 연결되어 다대다(N:M) 구조를 형성
    """

    # ---------------------------------------------------------
    # [3] 기본 키 (Primary Key)
    # ---------------------------------------------------------
    id = fields.IntField(pk=True)
    """
    동작 원리:
    - 자동 증가 정수형 기본 키
    """

    # ---------------------------------------------------------
    # [4] 질문 내용
    # ---------------------------------------------------------
    content = fields.TextField()
    """
    동작 원리:
    - TEXT 타입 컬럼 생성
    - 길이 제한 없음
    """

    # category 추가
    category = fields.CharField(max_length=50, null=True)

    # ---------------------------------------------------------
    # [5] 역참조: 이 질문을 받은 사용자 목록
    # ---------------------------------------------------------
    answered_by: fields.ReverseRelation["UserQuestion"]
    """
    동작 원리:
    - ReverseRelation은 실제 데이터 컬럼이 아님
    - Tortoise가 'question' FK를 가진 UserQuestion 모델을 기반으로 자동 생성하는 역참조
    - Question.answered_by → UserQuestion 객체 리스트로 접근 가능

    예:
        q = await Question.get(id=1).prefetch_related("answered_by")
        q.answered_by  -> [UserQuestion, UserQuestion, ...]
    """

    # ---------------------------------------------------------
    # [6] 문자열 표현 (관리자 UI/로그 확인용)
    # ---------------------------------------------------------
    def __str__(self):
        return self.content[:30]
    """
    동작 원리:
    - print(question) 호출 시 앞 30글자만 보여줌
    """


# =====================================================================
#  USERQUESTION MODEL  (N:M 매핑 테이블)
# =====================================================================
class UserQuestion(models.Model):                                         # [7] User ↔ Question 사이의 중간 매핑 테이블
    """
    USER_QUESTIONS 테이블
    - User와 Question 사이의 N:M 관계를 표현하는 JOIN TABLE
    - 추가 칼럼(answer_content, answered_at)까지 포함된 확장된 다대다 구조
    """

    # ---------------------------------------------------------
    # [8] 기본 키
    # ---------------------------------------------------------
    id = fields.IntField(pk=True)
    """
    단순한 자동 증가 PK
    """

    # ---------------------------------------------------------
    # [9] user_id → USERS 테이블 FK
    # ---------------------------------------------------------
    user = fields.ForeignKeyField(
        'models.User',
        related_name='assigned_questions'
    )
    """
    동작 원리:
    - FK 이름: user_id
    - UserQuestion.user → User 객체 반환
    - User.assigned_questions → UserQuestion 목록 역참조 활성화됨

    관계 구조: USERS ||--o{ USER_QUESTIONS
    """

    # ---------------------------------------------------------
    # [10] question_id → QUESTIONS 테이블 FK
    # ---------------------------------------------------------
    content = fields.ForeignKeyField(
        'models.Question',
        related_name='assigned_users'
    )
    """
    동작 원리:
    - FK 이름: question_id
    - UserQuestion.question → Question 객체 반환
    - Question.assigned_users → UserQuestion 목록 역참조

    관계 구조: QUESTIONS ||--o{ USER_QUESTIONS
    """

    # category 추가
    category = fields.CharField(max_length=50, null=True)

    # ---------------------------------------------------------
    # [11] 사용자의 답변 내용 (옵션)
    # ---------------------------------------------------------
    answer_content = fields.TextField(null=True)
    """
    동작 원리:
    - 사용자가 실제 질문에 대해 입력한 답변 내용 저장
    - null=True → 아직 답변하지 않은 상태도 허용
    """

    # ---------------------------------------------------------
    # [12] 답변 시간 (옵션)
    # ---------------------------------------------------------
    answered_at = fields.DatetimeField(null=True)
    """
    동작 원리:
    - 사용자가 답변한 날짜/시간 저장
    - null이면 아직 답변하지 않은 상태
    """

    # ---------------------------------------------------------
    # [13] 유니크 제약: User + Question 중복 할당 금지
    # ---------------------------------------------------------
    class Meta:
        unique_together = ("user", "content")
        """
        동작 원리:
        - 하나의 User가 같은 Question을 중복으로 배정받지 못하도록 하는 제약
        - 중복 삽입 시 IntegrityError 발생 → 중복 방지 확실
        - 실제 DB에는 복합 UNIQUE INDEX 생성:
              UNIQUE(user_id, question_id)
        """