# app/core/security.py (최종 정리 버전)

import bcrypt
import jwt
from datetime import datetime, timedelta, timezone
from typing import Optional
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from app.core.config import settings # 설정을 로드하여 SECRET_KEY와 ALGORITHM에 접근
from app.repositories.user_repo import UserRepository
from app.models.user import User

# 토큰을 추출할 경로 정의 (FastAPI 표준)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

# 1. 비밀번호 해싱 함수
def hash_password(password: str) -> str:
    """일반 비밀번호를 해시합니다."""
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed.decode('utf-8')

# 2. 비밀번호 검증 함수
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """일반 비밀번호와 해시된 비밀번호를 비교합니다."""
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

# 3. JWT 토큰 생성 함수
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """사용자 ID를 포함한 JWT 토큰을 생성합니다."""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire, "sub": str(data["user_id"])})
    
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

# 4. 사용자 인증을 위한 의존성 함수 (JWT 검증)
async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """JWT 토큰을 검증하고 현재 사용자 객체를 반환합니다."""
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # 1. 토큰 디코딩
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        user_id: int = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
    
    except jwt.PyJWTError:
        raise credentials_exception

    # 2. 사용자 ID로 DB에서 사용자 조회 (UserRepository.get_by_id는 user_repo.py에 정의되어야 함)
    user = await UserRepository.get_by_id(user_id)
    if user is None:
        raise credentials_exception
        
    return user