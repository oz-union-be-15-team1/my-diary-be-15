from tortoise import fields, models                                      # [1] ORM 필드/모델 import
from datetime import datetime, timezone                                  # [2] UTC 시간 처리용 datetime
from app.models.diary import Diary                                       # [3] 역참조 타입 힌트를 위해 import
from app.models.bookmark import Bookmark                                 # [4] 역참조 타입 힌트
from app.models.question import UserQuestion                             # [5] 역참조 타입 힌트


# =====================================================================
#  USER MODEL
# =====================================================================
class User(models.Model):                                                 # [6] USERS 테이블
    """
    USERS 테이블
    - 인증/로그인을 위한 계정 정보 저장
    - Diary, Bookmark, UserQuestion, TokenBlacklist 등 여러 테이블과 연관되는 중심 모델
    """

    # ---------------------------------------------------------
    # [7] Primary Key
    # ---------------------------------------------------------
    id = fields.IntField(pk=True)
    """
    자동 증가 정수형 Primary Key
    """

    # ---------------------------------------------------------
    # [8] username (unique)
    # ---------------------------------------------------------
    username = fields.CharField(max_length=50, unique=True)
    """
    동작 원리:
    - UNIQUE 제약 조건 생성
    - 같은 username을 가진 유저를 중복 저장 불가
    """

    # ---------------------------------------------------------
    # [9] password_hash
    # ---------------------------------------------------------
    password_hash = fields.CharField(max_length=255)
    """
    동작 원리:
    - 원본 비밀번호 저장 금지 → 반드시 해시 값 저장
    - passlib로 해싱한 값만 저장됨
    """

    # ---------------------------------------------------------
    # [10] email (nullable)
    # ---------------------------------------------------------
    email = fields.CharField(max_length=255, null=True)
    """
    null=True → 이메일을 선택 입력 가능
    """


    # ---------------------- 역참조 관계들 ----------------------

    # ---------------------------------------------------------
    # [11] diaries (User → Diary : 1:N)
    # ---------------------------------------------------------
    diaries: fields.ReverseRelation["Diary"]
    """
    동작 원리:
    - User.diaries → Diary 테이블에서 owner_id가 이 유저인 모든 레코드 반환
    - Diary 모델의 ForeignKeyField(owner=...)에서 자동 생성된 역참조
    - 실제 DB 컬럼은 Diary.owner_id로 존재함
    """

    # ---------------------------------------------------------
    # [12] token_entries (User → TokenBlacklist : 1:N)
    # ---------------------------------------------------------
    token_entries: fields.ReverseRelation["TokenBlacklist"]
    """
    동작 원리:
    - User.token_entries → 이 사용자가 로그아웃한 모든 토큰 목록 반환
    - TokenBlacklist.user FK가 기반이 됨
    """

    # ---------------------------------------------------------
    # [13] bookmarks (User → Bookmark : 1:N)
    # ---------------------------------------------------------
    bookmarks: fields.ReverseRelation["Bookmark"]
    """
    동작 원리:
    - User.bookmarks → 이 유저가 북마크한 모든 Bookmark 레코드 반환
    - Bookmark.user FK에서 자동 생성된 역참조
    """

    # ---------------------------------------------------------
    # [14] assigned_questions (User ↔ Question : N:M 매핑)
    # ---------------------------------------------------------
    assigned_questions: fields.ReverseRelation["UserQuestion"]
    """
    동작 원리:
    - User.assigned_questions → UserQuestion 객체들 반환
    - UserQuestion.user FK 기반
    - User ↔ Question 관계는 다대다이며, UserQuestion이 중간 매핑 테이블 역할
    """


# =====================================================================
#  TOKEN BLACKLIST MODEL
# =====================================================================
class TokenBlacklist(models.Model):                                       # [15] TOKEN_BLACKLIST 테이블
    """
    TOKEN_BLACKLIST 테이블
    - 로그아웃된 JWT / 강제로 무효화해야 하는 JWT를 저장하여 인증 강제 종료 기능 구현
    """

    # ---------------------------------------------------------
    # [16] Primary Key
    # ---------------------------------------------------------
    id = fields.IntField(pk=True)

    # ---------------------------------------------------------
    # [17] JWT Token 문자열
    # ---------------------------------------------------------
    token = fields.TextField()
    """
    동작 원리:
    - 실제 JWT 문자열 전체 저장
    - 길이가 고정되지 않기 때문에 TextField로 저장하는 것이 적절
    """

    # ---------------------------------------------------------
    # [18] user_id FK → USERS
    # ---------------------------------------------------------
    user = fields.ForeignKeyField(
        'models.User',
        related_name='token_entries'
    )
    """
    동작 원리:
    - TokenBlacklist.user → User 객체 반환
    - User.token_entries → 해당 유저가 블랙리스트에 넣은 모든 토큰 접근 가능
    - USERS ||--o{ TOKEN_BLACKLIST 구조 형성
    """

    # ---------------------------------------------------------
    # [19] expired_at (토큰 만료 시각 기록)
    # ---------------------------------------------------------
    expired_at = fields.DatetimeField(default=lambda: datetime.now(timezone.utc))
    """
    동작 원리:
    - 로그아웃 당시 서버 기준 시간 저장
    - JWT의 exp 값을 그대로 저장하거나, 나중에 정리 작업에 사용 가능
    - default=lambda: datetime.now(timezone.utc)
        → 모델 생성 시점의 UTC 시간을 동적으로 반영
        (default=datetime.now(...)라고 쓰면 "함수 실행 시점"이 아니라 "모듈 import 시점"의 시간이 들어가 버릴 위험 있음)
    """
