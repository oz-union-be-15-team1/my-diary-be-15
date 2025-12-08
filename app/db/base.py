# app/db/base.py

from app.core.config import settings
from typing import List
from urllib.parse import urlparse  # 💡 이 줄을 추가합니다!

# 1. TORTOISE_MODELS 리스트 정의 (기존과 동일)
TORTOISE_MODELS: List[str] = [
    # 기존 파일들
    "app.models.user", 
    "app.models.diary",
    "app.models.quote",
    "app.models.question", 
    "app.models.bookmark", 
    "aerich.models", 
]

# 2. DATABASE_URL을 파싱합니다.
# urlparse를 사용하여 URI를 host, port, user 등으로 분리합니다.
parsed_url = urlparse(settings.DATABASE_URL)
DB_CONFIG = {
    "host": parsed_url.hostname,
    "port": parsed_url.port,
    "user": parsed_url.username,
    "password": parsed_url.password,
    "database": parsed_url.path[1:], 
}


# 3. TORTOISE_ORM 딕셔너리 정의 (파싱된 값 사용)
TORTOISE_ORM = {
    "connections": {
        "default": {
            "engine": "tortoise.backends.asyncpg",
            # db_url 대신 파싱된 개별 매개변수를 전달합니다.
            "credentials": DB_CONFIG 
        }
    },
    
    "apps": {
        "models": {
            "models": TORTOISE_MODELS,  
            "default_connection": "default",
        }
    }
}