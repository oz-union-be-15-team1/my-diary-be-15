from pydantic import BaseModel

# 명언 생성 (POST 요청 본문) 시 사용되는 스키마
# 사용자가 명언을 DB에 추가할 때 필요한 데이터를 정의
class QuoteCreate(BaseModel):
    content: str
    author: str | None = None

# 명언 조회 (GET 요청 응답) 시 사용되는 스키마
# DB에서 조회된 명언 데이터의 구조를 정의하고, 클라이언트에게 반환될 때 사용
class QuoteResponse(BaseModel):
    id: int
    content: str
    author: str | None

    class Config:  # Pydantic 설정 클래스
        # ORM Mode 활성화:
        # SQLAlchemy/Tortoise ORM 모델 인스턴스에서
        # 속성 이름(예: quote_instance.id)으로 데이터를 가져올 수 있도록 한다
        from_attributes = True

# 북마크 조회 (GET 요청 응답) 시 사용되는 스키마
# 사용자의 북마크 목록을 조회할 때 반환되는 데이터의 구조를 정의
class QuoteBookmarkResponse(BaseModel):
    id: int
    # 북마크 객체에 명언 객체가 포함
    quote: QuoteResponse

    class Config: # Pydantic 설정 클래스
        from_attributes = True