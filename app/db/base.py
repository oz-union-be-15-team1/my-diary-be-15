from app.core.config import settings
from typing import List

# 💡 모델 파일 경로 정의: 프로젝트의 모든 모델을 여기에 명시합니다.
TORTOISE_MODELS: List[str] = [
    "app.models.user",  # 사용자(User) 모델 경로
    "app.models.diary",  # 다이어리(Diary) 모델 경로
    "app.models.quote",  # 명언(Quote) 모델 경로
    "app.models.question",  # 질문(Question) 모델 경로
    "app.models.token_blacklist",
    "aerich.models",  # Aerich 마이그레이션 도구 사용 시 필요한 모델
]

# Tortoise ORM 설정 딕셔너리
# settings.DATABASE_URL을 사용하여 PostgreSQL 연결 정보를 설정합니다.
TORTOISE_ORM = {
    "connections": {
        "default": settings.DATABASE_URL,
    },
    "apps": {
        "models": {
            "models": TORTOISE_MODELS,          # 위에 정의된 모든 ORM 모델 리스트
            "default_connection": "default",    # 사용할 DB 연결을 'default'로 지정
        }
    }
}
