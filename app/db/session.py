# app/db/session.py (ORM 초기화 로직 변경)

from tortoise.contrib.fastapi import register_tortoise
from app.db.base import TORTOISE_ORM
from tortoise import Tortoise

# Tortoise ORM을 초기화하고 FastAPI 앱에 연결합니다.
def init_tortoise(app):
    register_tortoise(
        app,
        config=TORTOISE_ORM, 
        generate_schemas=True,
    )
    
    # 💡 [핵심 추가] 시작 시 DB에 연결하고, 종료 시 DB 연결을 닫는 이벤트를 명시적으로 등록합니다.
    # Uvicorn은 FastAPI의 라이프사이클 이벤트를 사용하여 이 함수들을 호출합니다.
    
    @app.on_event("startup")
    async def startup_event():
        print("💡 DB 연결 시작 시도...")
        await Tortoise.init(config=TORTOISE_ORM)
        # 마이그레이션을 위한 테이블 생성 (선택 사항이지만 안전을 위해 추가)
        # await Tortoise.generate_schemas()
        print("✅ DB 연결 성공!")
        
    @app.on_event("shutdown")
    async def shutdown_event():
        print("🔌 DB 연결 종료 시도...")
        await Tortoise.close_connections()