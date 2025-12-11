from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from app.db.base import TORTOISE_ORM

def init_tortoise(app: FastAPI) -> None:
    """
    FastAPI 애플리케이션에 Tortoise ORM을 연결하고 startup/shutdown 이벤트를 등록합니다.
    """
    register_tortoise(
        app,
        config=TORTOISE_ORM,          # database.py에서 정의된 ORM 설정 사용
        generate_schemas=False,       # 💡 False로 설정하여 마이그레이션 도구(Aerich)를 통해 스키마 관리
        add_exception_handlers=True,  # DB 관련 예외 핸들러(404 등) 자동 등록
    )
