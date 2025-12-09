# app/core/config.py

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field # 필요하다면 Field 임포트 유지

class Settings(BaseSettings):
    # 💡 [필수] 데이터베이스 연결 URI 정의를 다시 추가합니다.
    DATABASE_URL: str = Field(..., description="PostgreSQL 연결 URI") 

    # 💡 [JWT 설정] (이전에 추가한 내용)
    SECRET_KEY: str = "YOUR_SECRET_KEY_MUST_BE_COMPLEX_AND_LONG"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # .env 파일에서 설정 로드
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

settings = Settings()