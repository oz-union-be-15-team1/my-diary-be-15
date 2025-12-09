from app.models.diary import Diary
from fastapi import HTTPException


class DiaryService:
    @staticmethod
    async def create(user, title, content):
        return await Diary.create(user=user, title=title, content=content)

    @staticmethod
    async def list_for_user(user):
        return await Diary.filter(user=user).all()

    @staticmethod
    async def get_or_404(diary_id: int):
        diary = await Diary.get_or_none(id=diary_id)
        if not diary:
            raise HTTPException(status_code=404, detail="Diary not found")
        return diary

    @staticmethod
    async def update(diary, data):
        diary.title = data.title or diary.title
        diary.content = data.content or diary.content
        await diary.save()
        return diary

    @staticmethod
    async def delete(diary):
        await diary.delete()
