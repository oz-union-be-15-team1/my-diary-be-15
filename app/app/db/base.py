# app/db/base.py

from app.core.config import settings

TORTOISE_ORM = {
    "connections": {
        "default": f"postgres://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
    },
    "apps": {
        "models": {
            "models": [
                "app.models.user",
                "app.models.diary",
                "app.models.bookmark",
                "app.models.quote",
                "app.models.question",
                "app.models.token_blacklist",
                "aerich.models",
            ],
            "default_connection": "default",
        },
    },
}
