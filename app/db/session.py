from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# 비동기 엔진(Engine) 생성
# settings.DATABASE_URL은 config.py에서 정의한 'postgresql+asyncpg://...' 형식의 URL입니다.
# pool_pre_ping=True는 연결 상태를 주기적으로 확인하여 끊어진 연결을 재활용하지 않도록 합니다.
async_engine = create_async_engine(
    settings.DATABASE_URL, 
    echo=settings.DEBUG,  # DEBUG=True이면 SQL 쿼리를 터미널에 출력합니다.
    pool_pre_ping=True
)

# 비동기 세션 클래스 생성
# expire_on_commit=False는 세션이 커밋된 후에도 객체를 사용할 수 있도록 합니다.
AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,  # 반드시 AsyncSession을 사용하도록 지정합니다.
    expire_on_commit=False,
)


# FastAPI 종속성 주입(Dependency Injection)을 위한 함수
# API 요청마다 독립적인 DB 세션을 제공하고, 요청이 완료되면 세션을 닫습니다.
async def get_db_session():
    """
    DB 세션을 제공하고, 사용 후 자동으로 세션을 닫는 비동기 제너레이터 함수.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            # 예외 발생 시 롤백 (FastAPI가 자동으로 처리할 수도 있지만 명시)
            await session.rollback()
            raise
        finally:
            # 세션 닫기
            await session.close()