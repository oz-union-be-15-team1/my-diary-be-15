from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.diary import DiaryCreate, DiaryResponse, DiaryUpdate
from app.services.diary_service import DiaryService
from app.core.security import get_current_user

router = APIRouter(prefix="/api/v1/diaries", tags=["Diaries"])

@router.post("/", response_model=DiaryResponse, status_code=status.HTTP_201_CREATED, description="create new diary")
async def create_diary(payload: DiaryCreate, current_user=Depends(get_current_user)):
    diary = await DiaryService.create(current_user, payload.title, payload.content)
    return diary

@router.get("/", response_model=list[DiaryResponse], description="get all diaries")
async def list_diaries(current_user=Depends(get_current_user)):
    return await DiaryService.list_for_user(current_user)

@router.get("/{diary_id}", response_model=DiaryResponse, description="get a diary by id")
async def get_diary(diary_id: int, current_user=Depends(get_current_user)):
    diary = await DiaryService.get_or_404(diary_id)
    if diary.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Forbidden")
    return diary

@router.put("/{diary_id}", response_model=DiaryResponse, description="update a diary by id")
async def update_diary(diary_id: int, payload: DiaryUpdate, current_user=Depends(get_current_user)):
    diary = await DiaryService.get_or_404(diary_id)
    if diary.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Forbidden")
    return await DiaryService.update(diary, payload)

@router.delete("/{diary_id}", description="delete a diary by id")
async def delete_diary(diary_id: int, current_user=Depends(get_current_user)):
    diary = await DiaryService.get_or_404(diary_id)
    if diary.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Forbidden")
    await DiaryService.delete(diary)
    return {"msg":"deleted"}
