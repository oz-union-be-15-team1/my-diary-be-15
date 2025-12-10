from fastapi import APIRouter, Depends # FastAPI의 핵심 기능인 APIRouter와 의존성 주입을 위한 Depends를 임포트
from app.schemas.user import UserCreate, UserLogin, UserResponse # Pydantic 모델: 사용자 생성, 로그인 요청, 응답 데이터 구조 정의
from app.services.auth_service import AuthService # 실제 인증 로직(비즈니스 로직)을 처리하는 서비스 클래스 임포트
from app.core.security import get_current_user # 현재 인증된 사용자 정보를 가져오는 의존성 함수 임포트 (보통 JWT 검증 로직 포함)

# 🚀 라우터 설정
# /auth 경로로 시작하는 모든 엔드포인트를 관리하며, 문서화 시 "Auth" 태그로 분류됨
router = APIRouter(prefix="/auth", tags=["Auth"])


# --- 인증 엔드포인트 정의 ---

@router.post(
    "/register", # HTTP POST 요청으로 /auth/register 경로에 접근
    response_model=UserResponse, # 성공 시 응답 데이터의 구조를 UserResponse Pydantic 모델로 검증
    description="register new user" # OpenAPI 문서(Swagger UI)에 표시될 설명
)
async def register_user(payload: UserCreate):
    """
    ## 동작 원리: 사용자 회원가입
    1. **요청 데이터 검증 (Pydantic):** 클라이언트로부터 받은 JSON 데이터(payload)가
       `UserCreate` 스키마(username, password, email)에 맞는지 **자동으로 검증**됩니다.
       (FastAPI의 강력한 기능)
    2. **비즈니스 로직 호출 (AuthService):** 검증된 데이터를 사용하여 `AuthService`의
       `register` 메서드를 **비동기적으로** 호출합니다.
       - 이 서비스 메서드 안에서 **실제 회원가입 로직** (예: 비밀번호 해싱, DB에 사용자 정보 저장 등)이 수행됩니다.
    3. **응답:** 서비스에서 성공적으로 생성된 **사용자 객체(토큰이 포함된)**를 반환합니다.
       FastAPI는 이 객체를 `UserResponse` 모델에 맞춰 JSON으로 변환하여 클라이언트에 전송합니다.
    """
    user = await AuthService.register(
        payload.username, # 요청 본문에서 사용자 이름 추출
        payload.password, # 요청 본문에서 비밀번호 추출
        payload.email # 요청 본문에서 이메일 추출
    )
    return user


@router.post(
    "/login", # HTTP POST 요청으로 /auth/login 경로에 접근
    response_model=UserResponse, # 성공 시 응답 데이터의 구조를 UserResponse Pydantic 모델로 검증
    description="login user" # OpenAPI 문서(Swagger UI)에 표시될 설명
)
async def login(payload: UserLogin):
    """
    ## 동작 원리: 사용자 로그인 및 인증 토큰 발급
    1. **요청 데이터 검증 (Pydantic):** 클라이언트로부터 받은 JSON 데이터(payload)가
       `UserLogin` 스키마(username, password)에 맞는지 **자동으로 검증**됩니다.
    2. **인증 로직 호출 (AuthService):** 검증된 사용자 이름과 비밀번호를 사용하여 `AuthService`의
       `authenticate` 메서드를 **비동기적으로** 호출합니다.
       - 이 서비스 메서드 안에서 **실제 로그인/인증 로직** (예: DB에서 사용자 검색, 해시된 비밀번호 비교, **JWT(JSON Web Token) 생성**)이 수행됩니다.
    3. **응답:** 인증에 성공하면 **토큰이 포함된** 사용자 객체를 반환합니다. 이 객체는 `UserResponse`에 맞춰 JSON으로 변환되어 클라이언트에 전송됩니다.
    """
    user = await AuthService.authenticate(payload.username, payload.password)
    return user


@router.get(
    "/me", # HTTP GET 요청으로 /auth/me 경로에 접근
    response_model=UserResponse, # 성공 시 응답 데이터의 구조를 UserResponse Pydantic 모델로 검증
    description="get user info" # OpenAPI 문서(Swagger UI)에 표시될 설명
)
async def get_me(user=Depends(get_current_user)):
    """
    ## 동작 원리: 현재 사용자 정보 조회 (보호된 라우트)
    1. **의존성 주입 (Depends):** 이 엔드포인트는 `user=Depends(get_current_user)`를 매개변수로 가집니다.
       - **FastAPI의 핵심!** 요청이 들어오면 핸들러 함수(`get_me`)가 실행되기 전에 먼저
         `get_current_user` 함수가 **자동으로 실행**됩니다.
    2. **인증 토큰 추출 및 검증 (`get_current_user` 동작):**
       - `get_current_user` 함수는 보통 요청 헤더에서 **Authorization: Bearer <token>** 형식의 **JWT**를 추출합니다.
       - 추출된 JWT의 **유효성** (서명, 만료 시간 등)을 검증하고, 토큰 내부에 담긴 **사용자 식별 정보**를 추출합니다.
       - 만약 토큰이 유효하지 않다면, 이 함수는 **HTTP Exception (예: 401 Unauthorized)**을 발생시켜 요청을 즉시 중단하고 클라이언트에 오류를 반환합니다.
    3. **사용자 객체 반환:** 토큰이 유효하면, `get_current_user`는 **인증된 사용자 객체**를 반환하고, 이 객체가 `get_me` 함수의 `user` 매개변수에 주입됩니다.
    4. **응답:** `get_me` 함수는 주입받은 `user` 객체를 그대로 반환하며, 이 객체는 `UserResponse` 모델에 맞춰 JSON으로 변환되어 클라이언트에 전송됩니다.
    """
    return user # 의존성 주입(Depends)을 통해 이미 인증된 사용자 객체를 반환