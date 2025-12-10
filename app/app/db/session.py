from fastapi import FastAPI                                        # [1] FastAPI 앱 객체 타입
from tortoise.contrib.fastapi import register_tortoise             # [2] FastAPI와 Tortoise ORM 연동 함수
from app.db.base import TORTOISE_ORM                               # [3] DB 설정이 들어 있는 ORM config 딕셔너리


def init_tortoise(app: FastAPI) -> None:
    """
    FastAPI 애플리케이션에 Tortoise ORM을 연결하고 startup/shutdown 이벤트를 등록하는 초기화 함수.

    동작 원리 요약:
    - register_tortoise()가 FastAPI의 lifecycle 이벤트(startup/shutdown)에 자동으로 훅(Hook)을 등록함
    - startup 시: DB 연결을 자동으로 생성
    - shutdown 시: DB 연결을 안전하게 종료
    - Aerich 기반 마이그레이션을 사용하기 위해 generate_schemas=False로 설정
    """

    # ---------------------------------------------------------
    # [4] Tortoise ORM 초기화 + FastAPI 이벤트 자동 등록
    # ---------------------------------------------------------
    register_tortoise(
        app,
        config=TORTOISE_ORM,            # [5] db/base.py에 정의된 DB 설정(JSON 형태)
        generate_schemas=False,         # [6] 스키마 자동 생성 비활성화 (Alembic/Aerich 사용하므로 False가 정석)
        add_exception_handlers=True,    # [7] Tortoise ORM 관련 예외를 FastAPI에 자동 등록 (404 등)
    )

    """
    🔍 register_tortoise() 내부 동작 상세 설명:

    1) FastAPI app에 다음 이벤트 리스너를 자동 등록:
        app.add_event_handler("startup", init_db_connection)
        app.add_event_handler("shutdown", close_db_connection)

    2) startup 시 Tortoise.init(config=...) 실행
       - DB Host/Port/User/Password/Models 경로를 모두 읽어 ORM 초기화
       - 모델 스캔 후 Tortoise 내부 메타데이터 생성

    3) generate_schemas=True인 경우:
       - Tortoise.generate_schemas()가 실행돼 DB 테이블을 직접 생성함
       - 하지만 우리는 Aerich(마이그레이션 도구)를 사용하므로 False가 정확함

    4) add_exception_handlers=True인 경우:
       - 모델 조회 실패 → DoesNotExist → 자동으로 HTTP 404로 변환
       - ValidationError 등 ORM 에러도 FastAPI Response로 변환됨

    즉, register_tortoise()는 단순히 DB 연결만 하는 게 아니라
    ✔ FastAPI App 생명주기에 자동 연결  
    ✔ 예외 핸들링 자동 추가  
    ✔ 모델 스캔 및 ORM 초기화  
    를 한 번에 처리하는 “ORM 전용 초기화 관리자”
    """

    # ---------------------------------------------------------
    # [8] 개발 편의를 위한 초기화 완료 메시지
    # ---------------------------------------------------------
    print("✅ Tortoise ORM 연결 및 이벤트 등록 완료.")
