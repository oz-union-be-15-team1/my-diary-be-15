from tortoise import fields, models                               # [1] Tortoise ORM의 필드 타입 및 모델 베이스 클래스 import


class Bookmark(models.Model):                                      # [2] Tortoise ORM의 Model 클래스 상속
    """
    BOOKMARKS 테이블 (N:M 관계를 위한 중간 테이블)

    동작 원리:
    - Bookmark는 User ↔ Quote 사이의 N:M 관계를 표현하는 ‘매핑 테이블’
    - 하나의 User는 여러 Quote를 북마크할 수 있고
      하나의 Quote도 여러 User에게 북마크될 수 있음
    - DB 관점에서는 'JOIN TABLE' (bridge table, mapping table)
    """

    # ---------------------------------------------------------
    # [3] 기본 키 (Primary Key)
    # ---------------------------------------------------------
    id = fields.IntField(pk=True)
    """
    동작 원리:
    - BOOKMARKS 테이블의 고유 식별자
    - Auto Increment Integer
    - 자동 생성됨 (기본키)
    """

    # ---------------------------------------------------------
    # [4] user_id (Foreign Key to User)
    # ---------------------------------------------------------
    user = fields.ForeignKeyField(
        'models.User',                # [4-1] FK가 참조할 모델 (lazy string referencing)
        related_name='bookmarks'      # [4-2] User.bookmarks 로 역참조 가능하게 설정
    )
    """
    동작 원리:
    - Bookmark.user → User 객체(1개)를 참조하는 관계
    - BOOKMARKS 테이블 내부에는 user_id INT 컬럼이 생성됨
    - User 객체에서도 user.bookmarks 로 북마크 목록을 조회하는 역방향 관계 자동 생성
    - 실질적으로 USER ||--o{ BOOKMARKS 관계를 구성
    """

    # ---------------------------------------------------------
    # [5] quote_id (Foreign Key to Quote)
    # ---------------------------------------------------------
    quote = fields.ForeignKeyField(
        'models.Quote',
        related_name='bookmarks'
    )
    """
    동작 원리:
    - Bookmark.quote → Quote 객체(1개)를 참조
    - BOOKMARKS.quote_id INT 컬럼 생성
    - Quote.bookmarks 로 해당 Quote를 북마크한 모든 User 조회 가능
    - QUOTES ||--o{ BOOKMARKS 관계 형성
    """

    # ---------------------------------------------------------
    # [6] 모델 메타 정보
    # ---------------------------------------------------------
    class Meta:
        unique_together = ("user", "quote")     # [6-1] 사용자/명언 중복 북마크 방지
        """
        동작 원리:
        - DB 차원에서 user_id + quote_id 조합이 유일하도록 제약조건 추가
        - 같은 User가 동일한 Quote를 두 번 북마크하려 하면
          → IntegrityError 발생 (Tortoise ORM에서도 예외 발생)
        - 즉, 북마크 중복을 완벽히 차단하는 기능
        """
