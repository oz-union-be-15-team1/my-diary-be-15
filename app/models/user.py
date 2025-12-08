from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator
from datetime import datetime

class User(models.Model):
    # USERS 테이블
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=50, unique=True)
    password_hash = fields.CharField(max_length=255)

    # 💡 관계 정의 (역참조 이름 설정)
    # user.diaries로 접근 가능
    diaries: fields.ReverseRelation["Diary"]

    # user.token_entries로 접근 가능
    token_entries: fields.ReverseRelation["TokenBlacklist"]

    # user.bookmarks로 접근 가능
    bookmarks: fields.ReverseRelation["Bookmark"]

    # user.assigned_questions로 접근 가능
    assigned_questions: fields.ReverseRelation["UserQuestion"]

    def __str__(self):
        return self.username

class TokenBlacklist(models.Model):
    # TOKEN_BLACKLIST 테이블
    id = fields.IntField(pk=True)
    token = fields.TextField()

    # 💡 관계 정의: user_id FK (USERS ||--o{ TOKEN_BLACKLIST)
    user = fields.ForeignKeyField('models.User', related_name='token_entries')

    expired_at = fields.DatetimeField(default=datetime.utcnow)

    def __str__(self):
        return f"Token for User {self.user_id}"