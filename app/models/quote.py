# app/models/quote.py (수정 후)

from tortoise import fields, models
from .bookmark import Bookmark # 💡 상대 경로로 수정: .bookmark

class Quote(models.Model):
    # QUOTES 테이블
    id = fields.IntField(pk=True)
    content = fields.TextField()
    author = fields.CharField(max_length=100, null=True)

    # 💡 관계 정의: 역참조 (이 명언을 북마크한 사용자들)
    users_bookmarking: fields.ReverseRelation["Bookmark"] # 문자열 참조이므로 오류 없음

    def __str__(self):
        return f"Quote by {self.author}"