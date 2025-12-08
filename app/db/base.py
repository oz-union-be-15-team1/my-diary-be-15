from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.declarative import declared_attr
from typing import Any

# 모든 모델이 상속받을 기본 클래스 정의
class Base(AsyncAttrs, DeclarativeBase):
    """
    SQLAlchemy의 DeclarativeBase를 상속받는 기본 클래스입니다.
    AsyncAttrs를 추가하여 비동기적인 접근자 기능을 사용할 수 있게 합니다.
    """
    __abstract__ = True  # 이 클래스는 테이블로 생성되지 않고, 다른 모델에 상속될 것임을 명시

    # 테이블 이름을 클래스 이름의 snake_case로 자동 생성하는 로직
    @declared_attr
    def __tablename__(cls) -> str:
        # User -> user, DiaryPost -> diary_post
        name = cls.__name__
        import re
        return re.sub(r'(?<!^)(?=[A-Z])', '_', name).lower()

    # 모든 모델에서 사용할 수 있는 공통 속성 정의 (예시)
    id: Any 

# 참고: 모델에서 사용할 모든 임포트 항목을 여기에 모아둘 수 있습니다.
# 예: from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Boolean
#     from sqlalchemy.orm import relationship