# app/schemas/question.py

from tortoise.contrib.pydantic import pydantic_model_creator
# Question 모델을 가져오기 위해 상대 경로 사용
from app.models.question import Question, UserQuestion 

# 💡 Question_Pydantic 스키마를 생성합니다. (필수)
# 이 이름이 app/api/v1/question.py에서 참조되고 있습니다.
Question_Pydantic = pydantic_model_creator(Question) 

# UserQuestion 스키마 (나중에 답변 API에 필요)
UserQuestion_Pydantic = pydantic_model_creator(UserQuestion)