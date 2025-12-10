from pydantic import BaseModel, Field                                    # [1] 입력 검증 및 직렬화 도구


# =====================================================================
# 1) UserCreate — 회원가입 요청(Request Body)
# =====================================================================
class UserCreate(BaseModel):                                             # [2] 회원가입 시 입력 받는 스키마
    """
    회원가입 시 클라이언트가 제공해야 하는 데이터 구조
    - username / password / email을 받음
    """

    username: str = Field(min_length=3, max_length=32)                   # [3] 사용자명 제한
    """
    동작 원리:
    - 최소 3자, 최대 32자
    - Field(...)가 없어도 필수(required) 필드로 처리됨
    """

    password: str = Field(min_length=3, max_length=32)                   # [4] 비밀번호 입력
    """
    동작 원리:
    - 평문(password)은 절대 DB에 저장하지 않음
    - Service 계층에서 hash_password()로 해싱하여 저장해야 함
    """

    email: str = Field(max_length=255)                                   # [5] 이메일
    """
    동작 원리:
    - 이메일 최대 길이 제한
    - EmailStr 타입을 사용하면 이메일 형식 검증도 가능함 (추천)
    """


# =====================================================================
# 2) UserLogin — 로그인 요청(Request Body)
# =====================================================================
class UserLogin(BaseModel):                                              # [6] 로그인 입력 구조
    """
    로그인 시 필요한 데이터 구조
    기본적으로 username + password만으로 충분하지만,
    email까지 필요하다면 서비스 정책에 따라 유지할 수 있음.
    """

    username: str                                                        # [7] 필수 입력
    password: str                                                        # [8] 필수 입력
    email: str                                                           # [9] (선택 사항 같지만 현재 필수 처리됨)

    """
    ⚠️ 중요: email을 로그인에서 요구하는 것이 일반적이지 않음
    
    업계 표준:
        - 로그인: username OR email + password
        - 회원가입: username + email + password

    로그인 시 email이 반드시 필요한 구조면 클라이언트가 매번 3개 입력해야 하므로
    UserLogin(email: Optional[str] = None )로 바꾸는 것을 권장함.
    """


# =====================================================================
# 3) UserResponse — 서버 응답(Response Body)
# =====================================================================
class UserResponse(BaseModel):                                           # [10] 사용자 정보 응답 스키마
    """
    서버가 클라이언트에게 반환하는 사용자 정보 구조
    비밀번호(password_hash)는 절대로 포함되지 않음
    """

    id: int                                                              # [11] 유저 고유 ID
    username: str                                                        # [12] 사용자명
    email: str                                                           # [13] 이메일

    class Config:
        from_attributes = True                                          # [14] ORM 객체 → Pydantic 자동 변환
        """
        from_attributes=True 동작 원리:

        ORM(User) 객체를 그대로 UserResponse 모델로 변환할 수 있음.
        
        예:
            user = await User.get(id=1)
            return UserResponse.model_validate(user)

        - dict() 변환 없이 attribute 값을 자동으로 읽음
        - password_hash는 모델에 없기 때문에 자동으로 제외됨 → 보안 유지
        """

