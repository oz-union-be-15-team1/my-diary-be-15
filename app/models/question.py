from tortoise import fields, models

class Question(models.Model):
    # QUESTIONS 테이블
    id = fields.IntField(pk=True)
    question_text = fields.TextField()

    # 💡 관계 정의: 역참조 (이 질문에 답변한 사용자 목록)
    answered_by: fields.ReverseRelation["UserQuestion"]

    def __str__(self):
        return self.question_text[:30]


class UserQuestion(models.Model):
    # USER_QUESTIONS 테이블 (사용자와 질문의 N:M 관계를 위한 중개 테이블)
    id = fields.IntField(pk=True)

    # 💡 관계 정의: user_id FK (USERS ||--o{ USER_QUESTIONS)
    user = fields.ForeignKeyField('models.User', related_name='assigned_questions')

    # 💡 관계 정의: question_id FK (QUESTIONS ||--o{ USER_QUESTIONS)
    question = fields.ForeignKeyField('models.Question', related_name='assigned_users')

    # (선택적 속성: 사용자가 이 질문에 대해 작성한 답변 내용 등)
    answer_content = fields.TextField(null=True)
    answered_at = fields.DatetimeField(null=True)

    class Meta:
        # User에게 같은 Question이 중복 할당되지 않도록 복합 인덱스 설정
        unique_together = ("user", "question")
