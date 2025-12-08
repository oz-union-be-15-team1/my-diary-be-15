from pydantic_settings import BaseSettings
from typing import Optional
from pathlib import Path

# 프로젝트의 루트 디렉토리 설정
# 현재 app/core/config.py 파일 위치를 기준으로 두 단계 위 (프로젝트 루트)
BASE_DIR = Path(__file__).resolve().parent.parent.parent

class Settings(BaseSettings):
    # 🔐 SECURITY
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # 🌐 SERVER CONFIG
    APP_NAME: str = "Diary Project"
    APP_ENV: str = "development"
    DEBUG: bool = True

    # 🍃 DATABASE (POSTGRES)
    # .env 파일에서 POSTGRES 관련 변수를 읽어 DATABASE_URL을 구성하는 방식
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_SERVER: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    
    # SQLAlchemy의 비동기 연결 URL 형식
    @property
    def DATABASE_URL(self) -> str:
        # asyncpg 드라이버를 위한 URL 구성
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    # 🧪 TEST DATABASE URL (선택적)
    TEST_DATABASE_URL: Optional[str] = None

    class Config:
        # 환경 변수 파일 경로 지정
        # 프로젝트 루트에 있는 .env 파일이나 .env.dev 파일을 읽도록 설정합니다.
        # .env 파일이 존재하지 않으면 .env.dev를 시도합니다.
        env_file = BASE_DIR / ".env.dev"  # 개발 환경을 기본으로 로드
        env_file_encoding = "utf-8"
        case_sensitive = True

# 전역 설정 객체 생성
settings = Settings()

# 예시: 설정이 제대로 로드되었는지 확인
# print(f"Database URL: {settings.DATABASE_URL}")
# print(f"App Environment: {settings.APP_ENV}")