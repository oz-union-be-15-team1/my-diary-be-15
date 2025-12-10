from pydantic_settings import BaseSettings, SettingsConfigDict  # [1] BaseSettings: .env/환경변수 자동 로딩 + 타입 캐스팅 기능 제공


class Settings(BaseSettings):  # [2] BaseSettings 상속 → 이 클래스는 “환경설정 자동 로딩 모델”로 동작함
    """
    동작원리 요약:
    - Settings() 객체가 생성되면 BaseSettings가 자동으로 다음 순서로 설정값을 읽는다:
        1) 코드에서 Settings(DB_USER="xxx") 형식으로 직접 전달된 값
        2) OS 시스템 환경변수 (export DB_USER=xxx)
        3) .env 파일 값
        4) .env.dev 파일 값
        5) 아래 정의된 기본값
    - 이후 Pydantic이 타입(str/int/bool)을 자동으로 변환(casting)해 준다.
    """

    # ----------------------
    # 🔹 데이터베이스 설정
    # ----------------------
    DB_USER: str = "postgres"      # [3] 기본값. 하지만 .env 또는 환경변수가 있으면 자동으로 override됨.
    DB_PASSWORD: str = "password"  # [4] BaseSettings가 .env의 같은 이름 키를 자동 매칭하여 읽는다.
    DB_HOST: str = "localhost"     # [5] 타입 힌트(str)에 맞춰 문자열로 유지.
    DB_PORT: int = 5432            # [6] .env에 "5433" 문자열이 있어도 int 변환됨(자동 타입 캐스팅).
    DB_NAME: str = "my_diary_db"   # [7]
    DATABASE_URL: str = ""         # [8] 전체 URL을 한 번에 넣을 경우 사용. 값이 있으면 db_url이 이걸 우선 반환함.

    # ----------------------
    # 🔹 JWT / 인증 관련 설정
    # ----------------------
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30             # [9] 숫자 변환 자동 처리됨.
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7   # [10] 파이썬 계산식 그대로 실행되어 10080 저장됨.

    # ----------------------
    # 🔹 앱 기본 설정
    # ----------------------
    APP_NAME: str = "my_app"      # [11]
    APP_ENV: str = "my_env"       # [12]
    DEBUG: bool = False           # [13] .env에 DEBUG=true 라고 문자열로 있어도 bool 변환됨.

    # ----------------------
    # 🔹 보안 설정
    # ----------------------
    ALGORITHM: str = "HS256"      # [14] JWT 암호화 알고리즘
    SECRET_KEY: str = ""          # [15] .env 파일에서 필수로 override되길 기대하는 필드

    # ----------------------
    # 🔹 동적 DB URL 생성 (핵심)
    # ----------------------
    @property
    def db_url(self) -> str:  # [16] FastAPI에서 DB 연결할 때 settings.db_url로 접근
        """
        동작원리:
        - DATABASE_URL 값이 설정되어 있으면 그대로 사용
            (Docker, Railway, Render 등 배포 환경에서 주로 이렇게 제공됨)
        - 없으면 개별 항목(DB_USER/DB_PASSWORD/DB_HOST/DB_PORT/DB_NAME) 조합해서 URL 생성
        """
        if self.DATABASE_URL:  # [17] .env 또는 환경변수에서 DATABASE_URL이 들어오면 우선 사용
            return self.DATABASE_URL

        # [18] 개별 항목을 조합해 PostgreSQL URL 생성
        return (
            f"postgres://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )


    # ----------------------
    # 🔹 BaseSettings 동작 설정 (가장 중요)
    # ----------------------
    model_config = SettingsConfigDict(  # [19]
        env_file=(".env", ".env.dev"),  # [20] Settings 생성 시 .env → .env.dev 순서로 파일을 읽음
        extra="ignore",                 # [21] .env에 정의되지 않은 추가 키가 있어도 오류 내지 않음
        env_prefix="",                  # [22] 환경변수 prefix 없음. (예: JWT_XXX 형태를 강제하려면 여기 넣음)
    )


# ----------------------
# 🔹 Settings 객체 생성
# ----------------------
settings = Settings()  # [23] ← 이 시점에 BaseSettings가 즉시 .env / 환경변수 전체를 읽어서 필드를 채움
"""
⚙️ Settings() 생성 시 실제 동작 과정:

1) .env 파일이 있으면 읽어서 key=value 로딩
2) .env.dev 도 읽는다 (env_file 튜플 순서대로)
3) OS 환경변수도 읽어서 동일한 키면 override
4) 코드 기본값과 merge하여 최종 settings 객체 완성
5) Pydantic이 타입 검사 + 변환 수행
"""
