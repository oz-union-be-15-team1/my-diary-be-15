from fastapi import HTTPException, status
from tortoise.exceptions import IntegrityError

from app.core.config import settings
from app.models.user import User
from app.models.token_blacklist import TokenBlacklist
from app.core.security import hash_password, verify_password, create_access_token, create_refresh_token
from datetime import datetime, timezone

class AuthService:
    @staticmethod
    async def register(username: str, password: str, email: str) -> User:
        hashed = hash_password(password)
        try:
            user = await User.create(
                username=username,
                password_hash=hashed,
                email=email
            )
            return user
        except IntegrityError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")

    @staticmethod
    async def authenticate(username: str, password: str) -> User:
        user = await User.get_or_none(username=username)
        if not user or not verify_password(password, user.password_hash):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        return user

    @staticmethod
    async def create_tokens_for_user(user: User):
        access = create_access_token(user.username)
        refresh = create_refresh_token(user.username)
        return {"access_token": access, "refresh_token": refresh, "token_type":"bearer"}

    @staticmethod
    async def logout(token: str, user: User):
        # decode to get exp
        from jose import jwt
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            exp = payload.get("exp")
            expired_at = datetime.fromtimestamp(exp, tz=timezone.utc) if exp else None
        except Exception:
            expired_at = None

        await TokenBlacklist.create(token=token, user=user, expired_at=expired_at)
