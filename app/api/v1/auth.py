# app/api/v1/auth.py (정리된 버전)

from fastapi import APIRouter, HTTPException
from app.services.auth_service import AuthService 
from app.schemas.user import UserInSchema, UserOutSchema, TokenOutSchema # 💡 스키마 이름 통일

# 💡 라우터 객체 정의
router = APIRouter(prefix="/auth", tags=["Authentication"]) 

@router.post(
    "/register",
    response_model=UserOutSchema, # 💡 통일된 스키마 이름 사용
    summary="새 사용자 계정 생성 (회원가입)"
)
async def register(user_data: UserInSchema): # 💡 통일된 스키마 이름 사용
    """
    새로운 사용자 계정을 생성하고 생성된 사용자 정보를 반환합니다.
    """
    # 💡 UserService에 user_data 객체 전체를 전달
    new_user = await AuthService.register_user(user_data=user_data) 
    
    # 💡 통일된 스키마 이름 사용
    return await UserOutSchema.from_tortoise_orm(new_user)
    
# 💡 로그인 엔드포인트는 여기에 정의해야 합니다.
@router.post(
    "/login", 
    response_model=TokenOutSchema, # 💡 통일된 스키마 이름 사용
    summary="사용자 로그인 및 JWT 토큰 발급"
)
async def login(user_data: UserInSchema): # 💡 통일된 스키마 이름 사용
    """
    사용자 이름과 비밀번호를 검증하고, 성공 시 JWT 토큰을 반환합니다.
    """
    token = await AuthService.login_for_access_token(
        username=user_data.username,
        password=user_data.password
    )
    return {"access_token": token, "token_type": "bearer"}