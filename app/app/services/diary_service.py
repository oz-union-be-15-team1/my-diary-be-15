from app.models.diary import Diary                                 # [1] Diary ORM 모델
from fastapi import HTTPException                                  # [2] 예외 처리용 (404 등)


class DiaryService:
    """
    Service 계층:
    - 비즈니스 로직을 수행하는 레이어
    - Router(Controller)와 ORM(Model) 사이에서 '중간 처리' 역할을 담당
    - 예외 처리, 권한 체크, 데이터 변환 등의 로직 포함 가능
    """


    # =====================================================================
    # 1) 일기 생성(Create)
    # =====================================================================
    @staticmethod
    async def create(user, title: str, content: str):
        """
        일기 생성 로직
        동작 원리:
        - Diary.create()는 ORM 레벨에서 INSERT 수행
        - owner=user 로 FK 연결됨
        - 반환값은 Diary ORM 객체
        """
        return await Diary.create(user=user, title=title, content=content)   # [3] DB에 새 레코드 생성


    # =====================================================================
    # 2) 특정 사용자의 일기 목록 조회(List)
    # =====================================================================
    @staticmethod
    async def list_for_user(user):
        """
        유저가 작성한 모든 Diary 조회
        동작 원리:
        - Diary.filter(user=user) → owner_id = user.id 인 Diary를 모두 가져옴
        - .all() → QuerySet 실행하여 리스트 반환
        """
        return await Diary.filter(user=user).all()                            # [4] 1:N 관계 조회


    # =====================================================================
    # 3) 일기 단건 조회(GET) — 없으면 404
    # =====================================================================
    @staticmethod
    async def get_or_404(diary_id: int):
        """
        Diary 단일 조회 로직
        동작 원리:
        - get_or_none() → 존재하지 않으면 None 반환
        - None이면 HTTP 404 예외 발생 → FastAPI에서 자동으로 JSON 응답 처리
        """
        diary = await Diary.get_or_none(id=diary_id)                          # [5] 단건 조회

        if not diary:
            raise HTTPException(status_code=404, detail="Diary not found")    # [6] 존재하지 않으면 404 반환

        return diary                                                          # [7] 정상 반환


    # =====================================================================
    # 4) 일기 수정(Update)
    # =====================================================================
    @staticmethod
    async def update(diary, data):
        """
        Diary 수정 로직
        동작 원리:
        - Patch 방식을 지원 (전달된 값만 수정)
        - data.title 또는 data.content가 None이면 기존 값 유지
        - save() 호출 시 ORM이 UPDATE SQL 실행
        """

        # [8] 전달된 값이 있을 때만 업데이트
        diary.title = data.title or diary.title
        diary.content = data.content or diary.content

        await diary.save()                                                    # [9] UPDATE 실행
        return diary                                                          # [10] 수정된 객체 반환


    # =====================================================================
    # 5) 일기 삭제(Delete)
    # =====================================================================
    @staticmethod
    async def delete(diary):
        """
        Diary 삭제 로직
        동작 원리:
        - ORM의 delete()는 DELETE SQL 실행
        - 객체 제거 후 return 없음
        """
        await diary.delete()                                                  # [11] DB에서 레코드 삭제
