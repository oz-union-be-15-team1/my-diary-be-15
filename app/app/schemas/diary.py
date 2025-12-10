from pydantic import BaseModel, Field                         # [1] 입력 검증 및 데이터 직렬화를 위한 Pydantic
from datetime import datetime                                # [2] created_at 필드 타입


# =====================================================================
#  1) DiaryCreate  —  일기 생성(Request Body)
# =====================================================================
class DiaryCreate(BaseModel):                                # [3] POST /diaries 입력 데이터 스키마
    """
    Diary 생성 시 클라이언트가 보내는 데이터 구조
    - title, content만 입력받음
    """

    title: str = Field(..., min_length=1)                    # [4] 필수 입력(...), 최소 1글자 이상
    """
    동작 원리:
    - ... → 필수(required) 필드임을 의미
    - min_length=1 → 빈 문자열("") 입력 시 ValidationError 발생
    """

    content: str                                             # [5] 필수 입력 (기본으로 required 처리됨)
    """
    동작 원리:
    - Pydantic은 타입 힌트만 있으면 기본값 없을 때 필수로 판단
    """


# =====================================================================
#  2) DiaryUpdate  —  일기 수정(Request Body)
# =====================================================================
class DiaryUpdate(BaseModel):                                # [6] PATCH/PUT 입력 스키마
    """
    Diary 수정 시 사용하는 스키마
    모든 필드를 Optional로 둬 부분 업데이트 가능(PATCH)
    """

    title: str | None = None                                 # [7] title은 수정할 수도, 건너뛸 수도 있음
    content: str | None = None                               # [8] content도 선택적 업데이트 가능
    """
    동작 원리:
    - Optional 필드는 None이 들어오면 "수정하지 않음"으로 처리 가능
    - Service 계층에서 조건부 업데이트 로직 구현에 적합함
    """


# =====================================================================
#  3) DiaryResponse  —  서버 응답(Response Body)
# =====================================================================
class DiaryResponse(BaseModel):                              # [9] GET/POST 응답 스키마(ORM 객체 직렬화)
    """
    클라이언트에게 반환되는 Diary 구조
    ORM 모델(Diary) 객체를 JSON으로 변환하는 데 사용됨
    """

    id: int                                                  # [10] Diary PK
    title: str                                               # [11] 제목
    content: str                                             # [12] 내용
    created_at: datetime                                     # [13] 작성 시각
    user_id: int                                             # [14] 소유자 ID(FK)

    class Config:
        from_attributes = True                               # [15] ORM 모델을 직접 변환 가능하게 설정
        """
        from_attributes=True 동작 원리:

        - Tortoise ORM 객체를 Pydantic 모델에 자동 매핑 가능하게 해주는 옵션
        - 예: 
                diary = await Diary.get(id=1)
                return DiaryResponse.model_validate(diary)

          → DiaryResponse가 Diary 객체의 필드 값을 자동으로 가져옴

        - Tortoise의 ORM 객체가 dict가 아니어도
          속성(attribute)을 읽어서 변환해주므로 매우 편리함.
        """
