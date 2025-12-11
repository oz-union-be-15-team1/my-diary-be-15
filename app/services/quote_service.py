import random
from typing import List
from fastapi import HTTPException, status

from app.models.quote import Quote
from app.models.user import User
from app.models.bookmark import Bookmark


class QuoteService:
    @staticmethod
    async def get_all() -> List[Quote]:
        # skip(offset)과 limit을 사용하여 페이징 처리
        quote = await Quote.all()
        if not quote:
            return []
        return quote

    @staticmethod
    async def get_random() -> Quote | None:
        # 전체 명언 개수 확인
        count = await Quote.all().count()
        if count == 0:
            return None

        # 파이썬 random을 사용하여 랜덤 인덱스 생성
        random_index = random.randint(0, count - 1)

        return await Quote.all().offset(random_index).first()


class QuoteBookmarkService:
    @staticmethod
    async def add_bookmark(current_user: User, quote_id: int) -> Bookmark:
        # 명언 존재 여부 확인
        quote = await Quote.get_or_none(id=quote_id)
        if not quote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Quote not found"
            )

        # 이미 북마크 되어 있는지 확인 (중복 방지)
        exists = await Bookmark.filter(user=current_user, quote=quote).exists()
        if exists:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Bookmark already exists"
            )

        # 북마크 생성
        bookmark = await Bookmark.create(user=current_user, quote=quote)
        return bookmark

    @staticmethod
    async def get_bookmarks(current_user: User) -> List[Bookmark]:
        # select_related("quote")를 사용하여 연관된 명언 정보를 한 번에 가져옴 (N+1 문제 방지)
        return await Bookmark.filter(user=current_user).select_related("quote")

    @staticmethod
    async def remove_bookmark(current_user: User, quote_id: int) -> None:
        # 해당 사용자의 해당 명언 북마크 삭제
        deleted_count = await Bookmark.filter(user=current_user, quote_id=quote_id).delete()

        if deleted_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Bookmark not found"
            )
