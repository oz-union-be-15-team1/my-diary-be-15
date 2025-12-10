from fastapi import HTTPException, status                               # [1] FastAPI 표준 예외 처리
from tortoise.exceptions import IntegrityError                          # [2] DB 중복/제약 조건 위반 시 발생

from app.core.config import settings                                    # [3] SECRET_KEY, TOKEN 만료시간 등 설정값
from app.models.user import User                                        # [4] User ORM 모델
from app.models.token_blacklist import TokenBlacklist                   # [5] 로그아웃된 토큰 저장용 모델
from app.core.security import (                                         # [6] 보안 관련 도구들
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token
)
from datetime import datetime, timezone                                 # [7] UTC 기반 시간 처리


class AuthService:
    """
    AuthService = 인증/인가 핵심 비즈니스 로직 계층

    - register → 회원가입 처리
    - authenticate → 로그인 검증
    - create_tokens_for_user → JWT 발급
    - logout → JWT 블랙리스트 등록
    """


    # =====================================================================
    # 1) 회원가입 (Register)
    # =====================================================================
    @staticmethod
    async def register(username: str, password: str, email: str) -> User:
        """
        회원가입 프로세스:
        1) 비밀번호 해싱
        2) User.create()로 DB 생성
        3) username 중복 시 IntegrityError 발생 → 400으로 변환
        """

        hashed = hash_password(password)                                 # [8] 패스워드 평문 → 해싱 변환

        try:
            user = await User.create(
                username=username,
                password_hash=hashed,
                email=email
            )
            return user                                                  # [9] 성공 → 사용자 객체 반환

        except IntegrityError:                                           # [10] username UNIQUE 위반
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User already exists"
            )


    # =====================================================================
    # 2) 로그인 인증 (Authenticate)
    # =====================================================================
    @staticmethod
    async def authenticate(username: str, password: str) -> User:
        """
        로그인 과정:
        1) username으로 사용자 조회
        2) 없으면 실패
        3) password_hash 검증
        4) 성공 시 User 모델 반환
        """

        user = await User.get_or_none(username=username)                # [11] 유저 존재 여부 확인

        if not user or not verify_password(password, user.password_hash):
            """
            실패 조건:
            - 사용자 없음
            - 패스워드 불일치
            → 동일하게 401 반환 (보안성: 어느 조건이 틀렸는지 노출 금지)
            """
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )

        return user                                                      # [12] 인증 성공


    # =====================================================================
    # 3) JWT 발급
    # =====================================================================
    @staticmethod
    async def create_tokens_for_user(user: User):
        """
        JWT 발급 구조:
        - Access Token: 짧은 만료시간(30분 등)
        - Refresh Token: 긴 만료시간(7일 등)
        - payload = {"sub": username, "exp": 만료시간}

        반환 형태:
        {
            "access_token": "...",
            "refresh_token": "...",
            "token_type": "bearer"
        }
        """

        access = create_access_token(user.username)                      # [13] Access Token 생성
        refresh = create_refresh_token(user.username)                    # [14] Refresh Token 생성

        return {
            "access_token": access,
            "refresh_token": refresh,
            "token_type": "bearer"
        }


    # =====================================================================
    # 4) 로그아웃 처리 — JWT 블랙리스트 등록
    # =====================================================================
    @staticmethod
    async def logout(token: str, user: User):
        """
        로그아웃 동작 원리:

        JWT는 원래 'stateless'라 서버가 강제로 무효화할 수 없음.
        → 해결: 블랙리스트 테이블(TokenBlacklist)에 토큰 저장

        get_current_user()에서 요청마다 블랙리스트를 확인해
        포함된 토큰은 즉시 401로 차단

        logout() 과정:
        1) 토큰 decode하여 exp(만료시간) 추출
        2) TokenBlacklist에 token, user_id, expired_at 저장
        3) 이후 해당 토큰은 어떤 API 요청에서도 절대 통과 불가
        """

        # ---------------------------------------------------------
        # [15] 토큰 exp 추출 (옵션)
        # ---------------------------------------------------------
        from jose import jwt                                            # 동적 import: 순환 import 방지

        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=[settings.ALGORITHM]
            )

            exp = payload.get("exp")                                    # [16] Unix timestamp
            expired_at = (
                datetime.fromtimestamp(exp, tz=timezone.utc)
                if exp else None
            )

        except Exception:
            """
            JWT decode 실패 시:
            - exp를 저장할 수 없지만 token 자체는 블랙리스트에 넣어야 함
            - expired_at=None 처리
            """
            expired_at = None

        # ---------------------------------------------------------
        # [17] 블랙리스트에 토큰 저장
        # ---------------------------------------------------------
        await TokenBlacklist.create(
            token=token,
            user=user,
            expired_at=expired_at
        )
        """
        이후 get_current_user()에서:
        
        if await is_token_blacklisted(token):
            raise 401

        이 로직으로 어떤 API 요청에서도 해당 토큰은 즉시 무효 처리됨.
        """
