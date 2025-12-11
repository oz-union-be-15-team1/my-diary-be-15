from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # 기본값 설정 (실제 값은 .env에서 읽어옴)
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "password"
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "my_diary_db"
    DATABASE_URL: str = ""

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    APP_NAME: str = "my_app"
    APP_ENV: str = "my_env"
    DEBUG: bool = False

    ALGORITHM: str = "HS256"
    SECRET_KEY: str = ""

    @property
    def db_url(self) -> str:
        if self.DATABASE_URL:
            return self.DATABASE_URL
        return (
            f"postgres://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    # FastAPI live session 코드 참고하여 수정
    model_config = SettingsConfigDict(
        env_file=(".env", ".env.dev"), # .env 파일 읽고 .env.dev 읽기
        extra="ignore",
        env_prefix="",  # 원하는 경우 "JWT_" 등 prefix를 둘 수 있음
    )

settings = Settings()
