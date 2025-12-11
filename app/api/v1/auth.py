from fastapi import APIRouter, Depends

from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, UserResponse, LoginResponse
from app.core.security import get_current_user, create_access_token, oauth2_scheme
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=UserResponse, description="register new user")
async def register_user(payload: UserCreate):
    user = await AuthService.register(
        payload.username,
        payload.password,
        payload.email
    )
    return user

@router.post("/login", response_model=LoginResponse, description="login user")
async def login(payload: UserLogin):
    user = await AuthService.authenticate(payload.username, payload.password)
    token = create_access_token(str(user.id))
    return {
        "access_token": token,
        "user": user
    }

@router.get("/me", response_model=UserResponse, description="get user info")
async def get_me(user=Depends(get_current_user)):
    return user

@router.post("/logout", description="logout user")
async def logout(
    current_user: User = Depends(get_current_user),
    token: str = Depends(oauth2_scheme)
):
    await AuthService.logout(token, current_user)
    return {"detail": "Successfully logged out"}
