from tortoise import fields, models                                      # [1] ORM 모델/필드 import


class TokenBlacklist(models.Model):                                      # [2] 로그아웃된 JWT를 저장하는 블랙리스트 테이블
    """
    TokenBlacklist 테이블의 역할:

    - JWT 기반 인증에서 문제가 되는 점:
        Access Token은 stateless(상태 없음) → 서버는 토큰을 강제로 무효화할 수 없음.
    - 해결 방법:
        로그아웃 시 해당 JWT 문자열을 DB에 저장하여 '사용 금지 상태'로 유지.
    - FastAPI의 get_current_user() 인증 로직에서 토큰이 블랙리스트에 있으면 즉시 401 반환.

    즉,
        "서버가 임의로 JWT를 폐기할 수 없는 문제를 해결하기 위한 강제 만료 저장소"
    """

    # ---------------------------------------------------------
    # [3] Primary Key
    # ---------------------------------------------------------
    id = fields.IntField(pk=True)
    """
    동작 원리:
    - 자동 증가 정수형 Primary Key
    - 개별 블랙리스트 레코드의 고유 ID
    """

    # ---------------------------------------------------------
    # [4] JWT Token 문자열
    # ---------------------------------------------------------
    token = fields.TextField()
    """
    동작 원리:
    - 실제 JWT 문자열 전체를 TEXT 타입으로 저장
    - 길이가 고정되지 않기 때문에 TextField가 적합
    - 같은 토큰이 다시 요청 오면 get_current_user()에서 즉시 인증 실패 처리

    예시:
        blacklist_entry.token = "eyJhbGciOiJIUzI1NiIsInR..."
    """

    # ---------------------------------------------------------
    # [5] FK: 이 토큰을 소유한 사용자
    # ---------------------------------------------------------
    user = fields.ForeignKeyField(
        "models.User",
        related_name="blacklisted_tokens"
    )
    """
    동작 원리:
    - TokenBlacklist.user → User 객체 반환
    - User.blacklisted_tokens → 이 유저가 로그아웃한 모든 토큰 목록 (역참조)
    - 관계 구조: USERS ||--o{ TOKEN_BLACKLIST

    사용 예:
        user = await User.get(id=1).prefetch_related("blacklisted_tokens")
        for t in user.blacklisted_tokens:
            print(t.token)
    """

    # ---------------------------------------------------------
    # [6] 토큰의 만료 시간(선택적)
    # ---------------------------------------------------------
    expired_at = fields.DatetimeField(null=True)
    """
    동작 원리:
    - JWT payload의 exp 값을 복사하거나,
      또는 서버에서 관리하려는 수명 정책을 적용할 때 사용 가능
    - null=True → 반드시 저장할 필요는 없음

    활용 예시:
        - 만료된 토큰을 주기적으로 자동 삭제하는 Cron 작업 구현 가능
        - 보안/로그 기록 용도로 사용 가능
    """

