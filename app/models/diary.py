from tortoise import fields, models
from datetime import datetime

class Diary(models.Model):
    # DIARIES 테이블
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=100)
    content = fields.TextField()
    created_at = fields.DatetimeField(default=datetime.utcnow)

    # 💡 관계 정의: user_id FK (USERS ||--o{ DIARIES)
    # related_name='diaries'는 User 모델에서 이미 사용됨
    owner = fields.ForeignKeyField('models.User', related_name='diaries')
