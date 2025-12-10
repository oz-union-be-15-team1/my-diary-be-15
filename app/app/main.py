# app/main.py (최종 정리 버전)

from fastapi import FastAPI                                                  # [1] FastAPI 앱 생성 핵심 클래스
from fastapi.middleware.cors import CORSMiddleware                           # [2] 브라우저 CORS 정책 해결용 미들웨어
from .db.session import init_tortoise                                        # [3] Tortoise ORM 초기화(Startup Hook 등록 함수)

# 라우터 직접 import (파일 이름 변경 없이)
from app.api.v1.question import router as question_router                    # [4] 질문 API 라우터
from app.api.v1.diary import router as diary_router                          # [5] 일기 API 라우터
from app.api.v1.auth import router as auth_router                            # [6] 인증 API 라우터
from app.api.v1.quote import router as quote_router                          # [7] 명언 API 라우터


# =====================================================================
# 1) FastAPI 앱 생성 (딱 1번만 해야 함)
# =====================================================================
app = FastAPI(
    title="My Diary API",                                                    # [8] 문서 제목 (Swagger UI)
    version="1.0.0",                                                         # [9] API 버전
    docs_url="/docs",                                                        # [10] Swagger UI 경로
    redoc_url=None                                                           # [11] ReDoc 비활성화
)
"""
[동작 원리 상세]
- FastAPI()를 호출하면 내부적으로 다음 구조가 생성된다:
    • routing table (엔드포인트 정보 저장)
    • middleware stack (미들웨어 체인)
    • event handlers (startup/shutdown hook)
    • dependency injection 컨테이너

- 앱은 반드시 '한 번만' 생성되어야 함.
  두 번 생성하면 앞의 설정이 덮어써져 DB 초기화·라우터 등록이 모두 무효가 됨.
"""


# =====================================================================
# 2) CORS 설정
# =====================================================================
app.add_middleware(
    CORSMiddleware,                                                          # [12] CORS 우회 미들웨어 삽입
    allow_origins=["*"],                                                     # [13] 모든 Origin 허용 (개발 환경)
    allow_credentials=True,                                                  # [14] 쿠키/인증 헤더 허용
    allow_methods=["*"],                                                     # [15] 모든 HTTP 메서드 허용
    allow_headers=["*"],                                                     # [16] 모든 요청 헤더 허용
)
"""
[동작 원리 상세]
- 브라우저 환경에서는 보안 정책(CORS) 때문에 다른 도메인에서 API 호출이 제한됨.
- CORSMiddleware가 HTTP 응답 헤더에 Access-Control-* 값을 자동 추가하여 문제를 해결함.
- allow_origins=["*"]은 개발환경에 적합하고,
  운영 환경에서는 특정 도메인만 허용하는 것이 보안적으로 안전함.
"""


# =====================================================================
# 3) Tortoise ORM 초기화 (startup 이벤트 등록)
# =====================================================================
init_tortoise(app)                                                           # [17] register_tortoise() 실행
"""
[동작 원리 상세]
- init_tortoise(app)은 다음을 수행한다:
    1) Tortoise.register_tortoise() 호출
    2) FastAPI 앱에 startup 이벤트 핸들러 추가
    3) FastAPI 앱에 shutdown 이벤트 핸들러 추가

✔ startup 시 실행되는 작업:
    - DB 연결 초기화 (Tortoise.init)
    - 모델 스캔 후 ORM 메타데이터 로드
    - 필요한 경우 generate_schemas 수행(우리는 False로 설정했으므로 Aerich 사용)

✔ shutdown 시 실행되는 작업:
    - DB 커넥션 안전하게 종료

즉, init_tortoise(app)은 즉시 DB에 연결하는 것이 아니라,
"FastAPI 실행 시점(startup 이벤트)에서 DB를 초기화하도록 예약"하는 함수이다.
"""


# =====================================================================
# 4) 라우터 등록 (prefix 포함)
# =====================================================================
app.include_router(question_router, prefix="/api/v1/questions")              # [18] 질문 API 전체 등록
app.include_router(diary_router, prefix="/api/v1/diaries")                   # [19] 일기 API 전체 등록
app.include_router(auth_router, prefix="/api/v1/auth")                       # [20] 인증 API 전체 등록
app.include_router(quote_router, prefix="/api/v1/quotes")                    # [21] 명언 API 전체 등록
"""
[동작 원리 상세]
- include_router()는 해당 라우터가 가진 모든 엔드포인트를 FastAPI 앱에 추가한다.
- prefix="/api/v1/xxx" 는 모든 엔드포인트 앞에 경로 접두사(prefix)를 자동으로 붙인다:

예)
    question_router 내부 → GET /random
    include_router(..., prefix="/api/v1/questions") 적용 후:
        최종 엔드포인트 = /api/v1/questions/random

- 라우터는 DB 초기화(init_tortoise) 이후에 등록되는 것이 일반적이다.
  (DB 초기화는 startup 이벤트에 등록되므로 실제 실행 순서는 문제 없음)

- Swagger 문서(/docs)는 등록된 모든 라우터의 메타데이터를 자동 스캔하여 UI에 표시한다.
"""


# ==========================
# 앱 초기화 완료
# ==========================
"""
결론:
- 앱 생성 → 미들웨어 → DB 초기화 예약 → 라우터 등록 → 서버 실행
- 이 main.py는 협업 규칙(파일명 유지, __init__.py 비움, 새 파일 생성 금지)을 완전히 만족하며,
  FastAPI의 공식적인 설계 흐름과도 100% 일치한다.
"""

