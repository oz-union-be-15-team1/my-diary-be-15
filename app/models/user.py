from tortoise import fields, models
from datetime import datetime, timezone
from diary import Diary
from bookmark import Bookmark
from question import UserQuestion

class User(models.Model):
    # USERS 테이블
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=50, unique=True)
    password_hash = fields.CharField(max_length=255)
    email = fields.CharField(max_length=255, unique=True)

    # 💡 관계 정의 (역참조 이름 설정)
    # user.diaries로 접근 가능
    diaries: fields.ReverseRelation["Diary"]

    # user.token_entries로 접근 가능
    token_entries: fields.ReverseRelation["TokenBlacklist"]

    # user.bookmarks로 접근 가능
    bookmarks: fields.ReverseRelation["Bookmark"]

    # user.assigned_questions로 접근 가능
    assigned_questions: fields.ReverseRelation["UserQuestion"]


class TokenBlacklist(models.Model):
    # TOKEN_BLACKLIST 테이블
    id = fields.IntField(pk=True)
    token = fields.TextField()

    # 💡 관계 정의: user_id FK (USERS ||--o{ TOKEN_BLACKLIST)
    user = fields.ForeignKeyField('models.User', related_name='token_entries')

    expired_at = fields.DatetimeField(default=lambda: datetime.now(timezone.utc))
