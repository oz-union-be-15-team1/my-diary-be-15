from datetime import datetime, timedelta, timezone               # [1] JWT 만료시간 계산용
from typing import Optional                                      # [2] Optional 타입 힌트

from jose import jwt, JWTError                                   # [3] JWT 인코딩/디코딩, 에러 처리
from passlib.context import CryptContext                         # [4] 비밀번호 해싱/검증용
from fastapi import Depends, HTTPException, status               # [5] 인증 실패 시 HTTP 예외 처리
from fastapi.security import OAuth2PasswordBearer                # [6] FastAPI가 JWT 토큰을 추출하기 위한 도구
from tortoise.exceptions import DoesNotExist                     # [7] ORM 조회 실패 시 발생하는 예외

from app.core.config import settings                             # [8] SECRET_KEY, 알고리즘, 만료시간 등 설정값 로딩
from app.models.user import User                                 # [9] 인증 후 반환할 User ORM 모델
from app.models.token_blacklist import TokenBlacklist            # [10] 로그아웃 시 저장되는 블랙리스트 테이블


# ---------------------------------------------------------
# [11] 비밀번호 해싱 알고리즘 설정
# ---------------------------------------------------------
pwd_context = CryptContext(
    schemes=["pbkdf2_sha256"], 
    # bcrypt보다 속도 빠르고 안전하며, 파이썬 기본 라이브러리 기반이기 때문에 호환성 높음
)

# ---------------------------------------------------------
# [12] OAuth2PasswordBearer: FastAPI가 Authorization 헤더에서 token을 자동 추출하는 의존성
# ---------------------------------------------------------
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")


# ---------------------------------------------------------
# [13] 비밀번호 해싱 함수
# ---------------------------------------------------------
def hash_password(password: str) -> str:
    """
    입력 비밀번호 → 해싱된 비밀번호로 변환
    DB에는 절대 원본 비밀번호가 저장되면 안 되므로 반드시 해싱 필요
    """
    return pwd_context.hash(password)


# ---------------------------------------------------------
# [14] 비밀번호 검증 함수
# ---------------------------------------------------------
def verify_password(plain: str, hashed: str) -> bool:
    """
    사용자가 로그인 시 제출한 plain 비밀번호와
    DB에 저장된 hashed 비밀번호가 일치하는지 확인
    """
    return pwd_context.verify(plain, hashed)


# ---------------------------------------------------------
# [15] Access Token 생성 함수
# ---------------------------------------------------------
def create_access_token(subject: str, expires_delta: Optional[timedelta] = None):
    """
    동작 원리:
    - subject: 보통 user_id 또는 username을 의미
    - exp: JWT 만료 시간 (Unix timestamp)
    - SECRET_KEY + ALGORITHM으로 서명된 JWT 문자열 반환
    - Access Token은 짧은 만료 시간(30분 등)을 가진다
    """
    if expires_delta is None:
        expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode = {
        "sub": str(subject),                                         # JWT Payload의 주체 (user 식별자)
        "exp": datetime.now(timezone.utc) + expires_delta            # 만료 시간
    }
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


# ---------------------------------------------------------
# [16] Refresh Token 생성 함수
# ---------------------------------------------------------
def create_refresh_token(subject: str, expires_delta: Optional[timedelta] = None):
    """
    동작 원리:
    - 역할: Access Token을 재발급하기 위한 장기 토큰
    - typ: "refresh" 를 추가하여 Access Token과 구분
    - 만료 기간: 일반적으로 7일 또는 그 이상
    """
    if expires_delta is None:
        expires_delta = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)

    to_encode = {
        "sub": str(subject),
        "exp": datetime.now(timezone.utc) + expires_delta,
        "typ": "refresh"                                             # Refresh Token임을 명시
    }
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


# ---------------------------------------------------------
# [17] Token Blacklist 검사
# ---------------------------------------------------------
async def is_token_blacklisted(token: str) -> bool:
    """
    동작 원리:
    - Logout 시 사용자의 JWT를 token_blacklist 테이블에 저장
    - 여기서 해당 token이 존재하면 → '이미 로그아웃된 토큰'
    - True = re-login 필요 / False = 정상 사용 가능
    """
    t = await TokenBlacklist.get_or_none(token=token)
    return t is not None


# ---------------------------------------------------------
# [18] JWT 검증 + User 로딩 (FastAPI 의존성)
# ---------------------------------------------------------
async def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    ⭐ 전체 인증 흐름 동작 원리 ⭐
    
    1) 클라이언트가 Authorization: Bearer <JWT> 헤더로 요청
    2) oauth2_scheme이 token 문자열만 추출
    3) get_current_user가 token을 입력받아 다음 로직 수행:
        - A. 블랙리스트 확인 (로그아웃된 토큰인지)
        - B. JWT 디코딩: SECRET_KEY와 ALGORITHM으로 서명 검증
        - C. 만료(exp) 확인
        - D. Payload에서 username(sub) 추출
        - E. DB에서 User 조회
    4) 어느 단계에서라도 실패하면 → 401 Unauthorized
    5) 성공하면 user 객체 반환 → 라우터 함수에서 의존성으로 사용
    """

    # 공통 예외 객체
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate":"Bearer"},
    )

    try:
        # STEP 1: 블랙리스트 확인
        if await is_token_blacklisted(token):
            raise credentials_exception

        # STEP 2: JWT 디코딩 + 서명 검증 + 만료 확인
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )

        username: str = payload.get("sub")
        if username is None:
            # JWT 형식은 맞지만 sub 필드가 없다면 위조 가능성
            raise credentials_exception

    except JWTError:
        # 디코딩 실패, 변조, 만료 등 JWT 관련 모든 오류 처리
        raise credentials_exception

    # STEP 3: DB에서 사용자 조회
    try:
        user = await User.get(username=username)

    except DoesNotExist:
        # Token의 유효성은 있지만 실제 유저가 존재하지 않는 경우
        raise credentials_exception

    # 인증 성공 → user 객체 반환
    return user
