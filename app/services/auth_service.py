# app/services/auth_service.py (전체 완성 버전 - 수정됨)

from fastapi import HTTPException
from app.repositories.user_repo import UserRepository
from app.models.user import User
from app.core.security import hash_password, verify_password, create_access_token
from app.schemas.user import UserInSchema # Pydantic 스키마 임포트
from datetime import timedelta
from app.core.config import settings
from typing import Optional

class AuthService:
    
    @staticmethod
    async def register_user(user_data: UserInSchema) -> User:
        """새 사용자를 등록하고 User 객체를 반환합니다."""
        
        # 1. 사용자명 중복 확인
        existing_user_by_name = await UserRepository.get_user_by_username(user_data.username) 
        if existing_user_by_name:
             raise HTTPException(status_code=400, detail="Username already registered.")
             
        # 💡 [필수 추가] 이메일 중복 확인
        # UserRepository에 get_user_by_email 함수가 있다고 가정합니다.
        existing_user_by_email = await UserRepository.get_user_by_email(user_data.email) 
        if existing_user_by_email:
             raise HTTPException(status_code=400, detail="Email address already registered.")

        # 2. 비밀번호 해싱 및 사용자 생성
        hashed_password = hash_password(user_data.password)
        
        # 3. 사용자 생성 (UserRepository 사용)
        try:
             user = await UserRepository.create_user(
                 username=user_data.username,
                 password_hash=hashed_password,
                 email=user_data.email
             )
             
             if not user:
                 raise HTTPException(status_code=500, detail="User creation failed in repository.")
             
             return user
             
        except Exception as e:
            # 예상치 못한 DB 오류 처리
            print(f"Error during registration: {e}")
            raise HTTPException(status_code=500, detail="Internal server error during user creation.")

    @staticmethod
    async def login_for_access_token(username: str, password: str) -> str:
        """사용자 인증 후 JWT 토큰을 반환합니다."""
        user = await UserRepository.get_user_by_username(username) # 💡 수정됨
        if not user or not verify_password(password, user.password_hash):
            raise HTTPException(status_code=401, detail="Incorrect username or password.")

        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"user_id": user.id}, expires_delta=access_token_expires
        )
        return access_token