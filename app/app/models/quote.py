from tortoise import fields, models                                       # [1] Tortoise ORM 기본 필드/모델 import
from app.models.bookmark import Bookmark                                  # [2] 역참조 타입 힌트를 위한 Bookmark import


class Quote(models.Model):                                                # [3] 명언(Quote) 테이블 모델
    """
    QUOTES 테이블
    - content: 명언 본문
    - author: 작성자
    - Bookmark 중간 테이블을 통해 User와 N:M 관계를 구성함
    """

    # ---------------------------------------------------------
    # [4] Primary Key
    # ---------------------------------------------------------
    id = fields.IntField(pk=True)
    """
    동작 원리:
    - 자동 증가 정수형 기본 키
    - DB에서 QUOTES.id 컬럼으로 생성됨
    """

    # ---------------------------------------------------------
    # [5] 명언 본문
    # ---------------------------------------------------------
    content = fields.TextField()
    """
    동작 원리:
    - TEXT 타입 컬럼 생성
    - 길이 제한 없음 → 긴 명언도 자유롭게 저장 가능
    """

    # ---------------------------------------------------------
    # [6] 작성자 (nullable)
    # ---------------------------------------------------------
    author = fields.CharField(max_length=100, null=True)
    """
    동작 원리:
    - VARCHAR(100) 컬럼 생성
    - null=True → 글쓴이가 없는 명언도 저장 가능
    """

    # ---------------------------------------------------------
    # [7] 역참조 관계: 이 명언을 북마크한 사용자들
    # ---------------------------------------------------------
    users_bookmarking: fields.ReverseRelation["Bookmark"]
    """
    동작 원리:
    - Bookmark 모델의 ForeignKeyField(quote)를 기준으로 자동 생성되는 역참조 관계
    - QUOTES ||--o{ BOOKMARKS (1:N 관계)이며, BOOKMARK는 User와 Quote를 연결하는 N:M 매핑 테이블

    실제로 생성되는 구조:
        BOOKMARKS 테이블:
            id          (PK)
            user_id     (FK → USERS)
            quote_id    (FK → QUOTES)

    Quote.users_bookmarking 의 의미:
        - 이 Quote를 북마크한 모든 Bookmark 레코드를 가져옴
        - 즉, 이 명언을 북마크한 사용자 목록을 간접적으로 조회 가능

    예시 사용법:
        quote = await Quote.get(id=1).prefetch_related("users_bookmarking")
        bookmarks = quote.users_bookmarking
        users = [bm.user for bm in bookmarks]

    주의:
        - ReverseRelation은 실제 DB 컬럼이 생성되지 않음
        - ORM 레벨에서 자동으로 연결된 "가상 필드"
    """




