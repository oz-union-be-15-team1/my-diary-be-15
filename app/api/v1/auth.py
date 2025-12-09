from fastapi import APIRouter, Depends
from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.services.auth_service import AuthService
from app.core.security import get_current_user

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserResponse, description="register new user")
async def register_user(payload: UserCreate):
    user = await AuthService.register(
        payload.username,
        payload.password,
        payload.email
    )
    return user


@router.post("/login", response_model=UserResponse, description="login user")
async def login(payload: UserLogin):
    user = await AuthService.authenticate(payload.username, payload.password)
    return user


@router.get("/me", response_model=UserResponse, description="get user info")
async def get_me(user=Depends(get_current_user)):
    return user
