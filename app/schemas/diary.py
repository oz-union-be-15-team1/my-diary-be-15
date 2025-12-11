from pydantic import BaseModel, Field
from datetime import datetime


class DiaryCreate(BaseModel):
    title: str = Field(..., min_length=1)
    content: str

class DiaryUpdate(BaseModel):
    title: str | None = None
    content: str | None = None

class DiaryResponse(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime
    user_id: int

    class Config:
        from_attributes = True
