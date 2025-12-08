from tortoise import fields, models

class Bookmark(models.Model):
    # BOOKMARKS 테이블 (N:M 관계를 위한 중개 테이블)
    id = fields.IntField(pk=True)

    # 💡 관계 정의: user_id FK (USERS ||--o{ BOOKMARKS)
    user = fields.ForeignKeyField('models.User', related_name='bookmarks')

    # 💡 관계 정의: quote_id FK (QUOTES ||--o{ BOOKMARKS)
    quote = fields.ForeignKeyField('models.Quote', related_name='bookmarks')

    class Meta:
        # User가 같은 Quote를 두 번 북마크하지 못하도록 복합 인덱스 설정 (선택적)
        unique_together = ("user", "quote")

    def __str__(self):
        return f"Bookmark by {self.user_id} for Quote {self.quote_id}"