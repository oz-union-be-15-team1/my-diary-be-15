# 📝 Daily Healing Log Project

사용자의 하루를 기록하고, 명언·질문을 통해 자기성찰을 돕는 **FastAPI 기반 백엔드 서비스**입니다.
회원가입 → 일기 작성 → 명언/질문 제공 → 북마크 → 배포까지 이어지는 실제 서비스 제작을 목표로 합니다.

---

# 📚 Project Index

* [1. 프로젝트 소개](#-프로젝트-소개)
* [2. 기술 스택](#-기술-스택)
* [3. 프로젝트 구조](#-프로젝트-구조)
* [4. ERD & 테이블 설명](#-erd--테이블-설명)
* [5. 모델(Model) 구조](#-모델model-구조)
* [6. API 명세](#-api-명세)
* [7. 웹 스크래핑 명언 저장](#-웹-스크래핑-명언-저장)
* [8. 테스트 코드](#-테스트-코드)
* [9. 배포(AWS EC2 + Nginx + Uvicorn)](#-배포aws-ec2--nginx--uvicorn)

---

# 📌 프로젝트 소개

Daily Healing Log는 사용자가 다음 기능을 사용할 수 있는 서비스입니다.

* 회원가입/로그인(JWT 기반 인증)
* 개인 일기 CRUD
* 랜덤 명언 제공 및 북마크 기능
* 랜덤 자기성찰 질문 제공
* 스크래핑 기반 명언 데이터 적재
* AWS EC2 배포

---

# 🛠 기술 스택

| 분야      | 기술                        |
| ------- | ------------------------- |
| Backend | FastAPI, Python 3.12      |
| DB      | MySQL / MariaDB           |
| ORM     | Tortoise ORM              |
| 인증      | JWT                       |
| 배포      | AWS EC2, Nginx, Uvicorn   |
| 테스트     | pytest, httpx.AsyncClient |
| 문서      | Swagger 자동 생성             |

---

# 📁 프로젝트 구조

```
project/
│── app/
│   ├── main.py
│   ├── models/
│   │   ├── user.py
│   │   ├── diary.py
│   │   ├── quote.py
│   │   ├── question.py
│   │   └── bookmark.py
│   ├── schemas/
│   │   ├── user.py
│   │   ├── diary.py
│   │   ├── quote.py
│   │   └── question.py
│   ├── routers/
│   │   ├── auth.py
│   │   ├── diaries.py
│   │   ├── quotes.py
│   │   └── questions.py
│   ├── services/
│   └── core/
│       ├── security.py
│       └── database.py
│
│── tests/
│── README.md
│── requirements.txt
```

---

# 🗂 ERD & 테이블 설명

프로젝트에 포함된 주요 도메인은 다음과 같습니다.

## 📌 ERD 이미지
![img_2.png](img_2.png)

## 📋 테이블 설명

| 테이블명                | 필드                                          | 설명            |
| ------------------- | ------------------------------------------- | ------------- |
| **users**           | id, email, password_hash, created_at        | 회원 정보 저장      |
| **token_blacklist** | id, token, user_id(FK), expired_at          | 로그아웃된 JWT 저장  |
| **diaries**         | id, title, content, created_at, user_id(FK) | 사용자 일기        |
| **quotes**          | id, content, author                         | 스크래핑 명언       |
| **bookmarks**       | id, user_id(FK), quote_id(FK)               | 명언 북마크        |
| **questions**       | id, question_text                           | 랜덤 자기성찰 질문    |
| **user_questions**  | id, user_id(FK), question_id(FK)            | 사용자가 받은 질문 기록 |

---

# 📦 모델(Model) 구조

Tortoise ORM을 활용하여 다음과 같은 관계를 정의합니다.

* User ⟶ Diary : **1:N**
* User ⟶ Bookmark : **1:N**
* Quote ⟶ Bookmark : **1:N**
* User ⟶ user_questions : **1:N**
* Question ⟶ user_questions : **1:N**

각 모델은 `models/` 디렉토리에 정리됩니다.

---

# 🔌 API 명세

주요 API 구조는 다음과 같습니다.

---

## 🧑‍💼 **사용자 인증 API**

### Signup

```
POST /api/auth/signup
```

Request

```json
{
  "email": "test@example.com",
  "password": "1234"
}
```

Response

```json
{
  "id": 1,
  "email": "test@example.com",
  "created_at": "2024-01-01T10:00:00"
}
```

---

## 📝 **일기 CRUD API**

### Create Diary

```
POST /api/diaries
Authorization: Bearer <token>
```

Request

```json
{
  "title": "오늘의 일기",
  "content": "정말 즐거운 하루였다!"
}
```

---

## 💬 **랜덤 명언 API**

### Get random quote

```
GET /api/quotes/random
```

### Add bookmark

```
POST /api/quotes/{quote_id}/bookmark
```

---

## ❓ **랜덤 질문 API**

### Get random question

```
GET /api/questions/random
```

---

# 🕸 웹 스크래핑 명언 저장

명언 출처: [https://saramro.com/quotes](https://saramro.com/quotes)

미션 수행 방식:

1. requests 또는 httpx 사용해 페이지 HTML 가져오기
2. BeautifulSoup으로 내용 파싱
3. DB 저장
4. API에서는 DB에서 랜덤 조회

---

# 🧪 테스트 코드

**pytest + pytest-asyncio + httpx.AsyncClient** 기반 테스트.

테스트 대상:

* 회원가입
* 로그인
* JWT 인증
* 일기 CRUD
* 명언 랜덤 조회
* 북마크 추가/삭제
* 권한 오류 처리

예시:

```python
async def test_signup(async_client):
    res = await async_client.post("/api/auth/signup", json={
        "email": "test@test.com",
        "password": "1234"
    })
    assert res.status_code == 201
```

---

# 🚀 배포 (AWS EC2 + NGINX + UVICORN)

배포 플로우:

1. EC2 생성 (Ubuntu 24.04)
2. SSH 접속
3. Python & venv 설치
4. 프로젝트 clone
5. uvicorn 실행해 동작 확인
6. Nginx 리버스 프록시 연결
7. 서비스 자동 실행 (systemd)

예시 systemd 설정:

```
[Service]
ExecStart=/usr/bin/python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always
```

접속:

```
http://<EC2_PUBLIC_IP>
```

---

# 🎉 마무리

이 프로젝트는 FastAPI의 핵심 기능(라우팅, 인증, ORM, DB, 테스트, 배포)을 모두 포함한 **완성형 백엔드 서비스**입니다.
여기에 기능 확장, 캐싱, Docker 배포 등 다양한 기능을 더해 성장시킬 수 있습니다.

---
