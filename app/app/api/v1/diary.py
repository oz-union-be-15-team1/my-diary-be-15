from fastapi import APIRouter, Depends, HTTPException, status # FastAPI의 핵심 기능(라우터, 의존성 주입, 예외 처리, HTTP 상태 코드) 임포트
from app.schemas.diary import DiaryCreate, DiaryResponse, DiaryUpdate # Pydantic 모델: 다이어리 생성/수정 요청, 응답 데이터 구조 정의
from app.services.diary_service import DiaryService # 실제 다이어리 데이터 로직(비즈니스 로직)을 처리하는 서비스 클래스 임포트
from app.core.security import get_current_user # 현재 인증된 사용자 정보를 가져오는 의존성 함수 임포트 (보통 JWT 검증 로직 포함)

# 🚀 라우터 설정
# /api/v1/diaries 경로로 시작하는 모든 엔드포인트를 관리하며, 문서화 시 "Diaries" 태그로 분류됨
router = APIRouter(prefix="/api/v1/diaries", tags=["Diaries"])

# --- 다이어리 CRUD 엔드포인트 정의 ---

@router.post(
    "/", # HTTP POST 요청으로 /api/v1/diaries/ 경로에 접근
    response_model=DiaryResponse, # 성공 시 응답 데이터의 구조를 DiaryResponse Pydantic 모델로 검증
    status_code=status.HTTP_201_CREATED, # 성공 시 HTTP 201 Created 상태 코드를 반환하도록 명시
    description="create new diary" # OpenAPI 문서(Swagger UI)에 표시될 설명
)
async def create_diary(payload: DiaryCreate, current_user=Depends(get_current_user)):
    """
    ## 동작 원리: 다이어리 생성
    1. **인증 확인 (Depends):** 요청이 들어오면 `get_current_user`가 먼저 실행됩니다.
       - JWT 토큰을 검증하고 **인증된 사용자 객체**를 `current_user`에 주입합니다.
       - 인증 실패 시 **401 Unauthorized** 예외가 발생하여 요청이 중단됩니다.
    2. **요청 데이터 검증 (Pydantic):** 클라이언트로부터 받은 `payload`가 `DiaryCreate` 스키마(title, content)에 맞는지 자동으로 검증됩니다.
    3. **비즈니스 로직 호출 (DiaryService):** `DiaryService.create`를 호출하여 다이어리를 생성합니다.
       - **핵심:** `current_user` 객체를 전달하여 새로 생성되는 다이어리가 **현재 사용자에게 연결**되도록 합니다. (인가: 누가 생성하는가?)
    4. **응답:** 생성된 다이어리 객체를 반환하며, 201 상태 코드가 반환됩니다.
    """
    diary = await DiaryService.create(current_user, payload.title, payload.content)
    return diary

# ----------------------------------------------------

@router.get(
    "/", # HTTP GET 요청으로 /api/v1/diaries/ 경로에 접근
    response_model=list[DiaryResponse], # 성공 시 응답은 DiaryResponse 객체의 리스트여야 함
    description="get all diaries" # OpenAPI 문서(Swagger UI)에 표시될 설명
)
async def list_diaries(current_user=Depends(get_current_user)):
    """
    ## 동작 원리: 사용자별 다이어리 목록 조회
    1. **인증 확인 (Depends):** `get_current_user`를 통해 인증된 사용자 객체(`current_user`)를 확보합니다.
    2. **비즈니스 로직 호출 (DiaryService):** `DiaryService.list_for_user(current_user)`를 호출합니다.
       - 이 서비스 메서드는 데이터베이스에서 **오직 `current_user`가 작성한** 다이어리 목록만을 필터링하여 가져옵니다. (인가: 자신의 데이터만 조회)
    3. **응답:** 조회된 다이어리 리스트를 반환합니다.
    """
    return await DiaryService.list_for_user(current_user)

# ----------------------------------------------------

@router.get(
    "/{diary_id}", # HTTP GET 요청으로 /api/v1/diaries/{diary_id} 경로에 접근
    response_model=DiaryResponse, # 성공 시 응답 데이터의 구조를 DiaryResponse Pydantic 모델로 검증
    description="get a diary by id" # OpenAPI 문서(Swagger UI)에 표시될 설명
)
async def get_diary(diary_id: int, current_user=Depends(get_current_user)):
    """
    ## 동작 원리: 특정 다이어리 조회 및 소유권 검사
    1. **인증 확인 (Depends):** `current_user` 객체를 확보합니다.
    2. **리소스 조회 (DiaryService):** `DiaryService.get_or_404(diary_id)`를 호출합니다.
       - 해당 ID의 다이어리가 없으면, 서비스 계층에서 **HTTPException 404 Not Found**를 발생시켜 요청을 중단시킵니다.
    3. **인가 (소유권 검사):** 조회된 다이어리의 `user_id`와 `current_user.id`를 비교합니다.
       - **핵심:** `if diary.user_id != current_user.id:`
       - 만약 두 ID가 다르면, 사용자가 **다른 사람의 다이어리에 접근**하려 한 것이므로,
         `raise HTTPException(status_code=403, detail="Forbidden")`을 통해 **403 Forbidden** 예외를 발생시켜 접근을 차단합니다.
    4. **응답:** 소유권이 확인되면 다이어리 객체를 반환합니다.
    """
    diary = await DiaryService.get_or_404(diary_id)
    if diary.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Forbidden") # 403: 접근 권한 없음
    return diary

# ----------------------------------------------------

@router.put(
    "/{diary_id}", # HTTP PUT 요청으로 /api/v1/diaries/{diary_id} 경로에 접근
    response_model=DiaryResponse, # 성공 시 응답 데이터의 구조를 DiaryResponse Pydantic 모델로 검증
    description="update a diary by id" # OpenAPI 문서(Swagger UI)에 표시될 설명
)
async def update_diary(diary_id: int, payload: DiaryUpdate, current_user=Depends(get_current_user)):
    """
    ## 동작 원리: 다이어리 수정 및 소유권 검사
    1. **인증 및 조회:** `get_diary`와 동일하게 인증된 사용자를 확인하고, 다이어리를 조회합니다 (404 처리 포함).
    2. **인가 (소유권 검사):** `if diary.user_id != current_user.id:`를 통해 현재 사용자가 다이어리의 소유자인지 확인합니다.
       - 소유자가 아니면 **403 Forbidden** 예외를 발생시킵니다.
    3. **비즈니스 로직 호출 (DiaryService):** `DiaryService.update(diary, payload)`를 호출합니다.
       - 조회된 `diary` 객체와 수정 요청 데이터(`payload`)를 사용하여 DB의 데이터를 업데이트합니다.
    4. **응답:** 수정된 다이어리 객체를 반환합니다.
    """
    diary = await DiaryService.get_or_404(diary_id)
    if diary.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Forbidden")
    return await DiaryService.update(diary, payload)

# ----------------------------------------------------

@router.delete(
    "/{diary_id}", # HTTP DELETE 요청으로 /api/v1/diaries/{diary_id} 경로에 접근
    description="delete a diary by id" # OpenAPI 문서(Swagger UI)에 표시될 설명
)
async def delete_diary(diary_id: int, current_user=Depends(get_current_user)):
    """
    ## 동작 원리: 다이어리 삭제 및 소유권 검사
    1. **인증 및 조회:** `get_diary`와 동일하게 인증된 사용자를 확인하고, 다이어리를 조회합니다 (404 처리 포함).
    2. **인가 (소유권 검사):** `if diary.user_id != current_user.id:`를 통해 현재 사용자가 다이어리의 소유자인지 확인합니다.
       - 소유자가 아니면 **403 Forbidden** 예외를 발생시킵니다.
    3. **비즈니스 로직 호출 (DiaryService):** `DiaryService.delete(diary)`를 호출하여 DB에서 해당 다이어리를 제거합니다.
    4. **응답:** 성공 메시지를 포함한 JSON 객체를 반환합니다. (HTTP 200 OK 상태 코드)
    """
    diary = await DiaryService.get_or_404(diary_id)
    if diary.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Forbidden")
    await DiaryService.delete(diary)
    return {"msg":"deleted"} # 삭제 성공 메시지 반환