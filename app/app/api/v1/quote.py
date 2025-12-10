# app/api/v1/quote.py

from fastapi import APIRouter
from app.models.quote import Quote
from app.schemas.quote import Quote_Pydantic

# 🔥 FastAPI 라우터 생성 (이게 있어야 main.py에서 import 가능)
router = APIRouter(
    tags=["Quotes"]
)

# -------------------------------------------
# 1) 전체 명언 조회
# -------------------------------------------
@router.get("/", summary="모든 명언 조회", response_model=list[Quote_Pydantic])
async def list_quotes():
    quotes = await Quote.all()
    return await Quote_Pydantic.from_queryset(quotes)


# -------------------------------------------
# 2) 특정 명언 조회
# -------------------------------------------
@router.get("/{quote_id}", summary="특정 명언 조회", response_model=Quote_Pydantic)
async def get_quote(quote_id: int):
    quote = await Quote.get(id=quote_id)
    return await Quote_Pydantic.from_tortoise_orm(quote)
