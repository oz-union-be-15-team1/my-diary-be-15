from fastapi import APIRouter, Depends, Query, HTTPException
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.quote import QuoteBookmarkResponse, QuoteResponse
from app.scraping.quote_scraper import scrape_and_save_quotes
from app.services.quote_service import QuoteBookmarkService, QuoteService


router = APIRouter(prefix="/quotes", tags=["Quotes"])

""" #######################################
################ 명언 ######################
####################################### """
@router.get(
    "",
    response_model=list[QuoteResponse],
    summary="전체 명언 조회",
    description="DB에 저장된 모든 명언 조회",
)
async def get_all_quotes():
    quotes = await QuoteService.get_all()
    return quotes


@router.get(
    "/random",
    response_model=QuoteResponse,
    summary="랜덤 명언 조회",
    description="DB에서 랜덤으로 명언 1개 조회",
)
async def get_random_quote():
    quote = await QuoteService.get_random()
    if not quote:
        raise HTTPException(status_code=404, detail="No quotes found")
    return quote


""" #######################################
############ 명언 북마크 #####################
####################################### """
@router.post(
    "/{quote_id}/bookmark",
    response_model=QuoteBookmarkResponse,
    summary="명언 북마크 추가",
    description="명언을 북마크에 추가 (중복x)",
)
async def add_bookmark(
    quote_id: int,
    current_user: User = Depends(get_current_user),
):
    bookmark = await QuoteBookmarkService.add_bookmark(current_user, quote_id)
    await bookmark.fetch_related("quote")
    return bookmark


@router.get(
    "/bookmarks",
    response_model=list[QuoteBookmarkResponse],
    summary="내 북마크 목록 조회",
    description="로그인한 사용자의 북마크 목록 조회",
)
async def get_my_bookmarks(
    current_user: User = Depends(get_current_user),
):
    bookmarks = await QuoteBookmarkService.get_bookmarks(current_user)
    return bookmarks


@router.delete(
    "/{quote_id}/bookmark",
    summary="북마크 해제",
    description="북마크에서 명언 제거",
)
async def remove_bookmark(
    quote_id: int,
    current_user: User = Depends(get_current_user),
):
    await QuoteBookmarkService.remove_bookmark(current_user, quote_id)
    return {"message": "북마크가 성공적으로 삭제되었습니다"}


""" #######################################
############ 명언 스크랩 #####################
####################################### """
@router.post(
    "/scrape",
    summary="명언 스크래핑",
    description="saramro.com에서 명언을 스크래핑하여 DB에 저장",
)
async def scrape_quotes(
    # pages: int = Query(default=10, ge=1, le=100, description="스크래핑할 페이지 수"),
    pages: int = Query(default=10, ge=1, le=100, description="스크래핑할 페이지 수"),
):
    result = await scrape_and_save_quotes(pages)
    return result