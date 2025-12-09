# app/repositories/user_repo.py (최종 수정)

from app.models.user import User
# ❌ from app.services.security import hash_password # 이 줄을 삭제합니다.
from typing import Optional

class UserRepository:
    """사용자 데이터베이스 접근 로직을 담당합니다."""
    
    @staticmethod
    async def get_user_by_username(username: str) -> Optional[User]:
        """사용자 이름으로 사용자를 조회합니다."""
        return await User.filter(username=username).first()
    
    @staticmethod
    async def get_user_by_email(email: str) -> Optional[User]: # 💡 이 함수를 추가합니다.
        """이메일로 사용자를 조회합니다."""
        return await User.filter(email=email).first()
    
    @staticmethod
    async def get_by_id(user_id: int) -> Optional[User]: # 💡 이 함수를 추가합니다.
        """ID로 사용자를 조회합니다."""
        return await User.filter(id=user_id).first()
    @staticmethod
    # 💡 인수를 'password_hash'로 수정하여 서비스 계층과 일치시킵니다.
    async def create_user(username: str, password_hash: str, email: str) -> User: 
        """새로운 사용자 계정을 생성합니다. (이미 해시된 비밀번호를 받습니다)"""
        # ❌ password_hash = hash_password(password) # 이 해싱 로직을 제거합니다.
        
        user = await User.create(
            username=username,
            password_hash=password_hash, # 💡 이미 해시된 비밀번호를 바로 사용
            email=email
        )
        return user