from tortoise import fields, models                                       # [1] ORM 필드/모델 import
from datetime import datetime                                             # [2] created_at 기본값 설정용


class Diary(models.Model):                                                # [3] Tortoise ORM의 Model 기반 클래스
    """
    DIARIES 테이블 (User → Diary: 1:N 관계)

    동작 원리 요약:
    - 하나의 User는 여러 Diary를 가질 수 있는 구조 (1:N)
    - Diary는 항상 특정 User에 속함 (owner FK)
    - Tortoise ORM은 FK를 통해 자동 역참조(User.diaries)도 생성함
    """

    # ---------------------------------------------------------
    # [4] Primary Key: id
    # ---------------------------------------------------------
    id = fields.IntField(pk=True)
    """
    동작 원리:
    - 자동 증가(Auto Increment) 정수형 PK
    - DB 테이블의 고유 식별자 역할
    """

    # ---------------------------------------------------------
    # [5] 제목(title)
    # ---------------------------------------------------------
    title = fields.CharField(max_length=100)
    """
    동작 원리:
    - VARCHAR(100) 컬럼 생성
    - 제목 길이 제한으로 DB 저장 안정성 확보
    """

    # ---------------------------------------------------------
    # [6] 내용(content)
    # ---------------------------------------------------------
    content = fields.TextField()
    """
    동작 원리:
    - TEXT 타입 컬럼 생성
    - 길이 제한 없음 (매우 긴 일기 내용도 저장 가능)
    """

    # ---------------------------------------------------------
    # [7] 생성일시(created_at)
    # ---------------------------------------------------------
    created_at = fields.DatetimeField(default=datetime.utcnow)
    """
    동작 원리:
    - default=datetime.utcnow → Diary 객체 생성 시 자동 실행됨(UTC 기준)
    - DB에서 기본값이 아니라, Python 레벨에서 기본값을 넣음
    - timezone-aware 필드가 필요하면 datetime.now(timezone.utc) 형태로 변경 가능
    """

    # ---------------------------------------------------------
    # [8] Foreign Key: owner(user_id)
    # ---------------------------------------------------------
    owner = fields.ForeignKeyField(
        'models.User',                   # [8-1] User 모델을 FK로 참조 (lazy string)
        related_name='diaries'           # [8-2] User.diaries 로 역참조 가능하게 설정
    )
    """
    동작 원리:
    - DIARIES 테이블에 owner_id INT 컬럼 생성됨
    - Diary.owner → User 객체 반환 (1개)
    - User.diaries → 해당 유저가 작성한 모든 Diary 리스트 반환 (1:N 역참조)
    - 관계 구조: USERS ||--o{ DIARIES (User 하나 → Diary 여러 개)
    """

