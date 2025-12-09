# app/schemas/user.py (UserInSchema로 통일하여 정의)

from pydantic import BaseModel, Field
from tortoise.contrib.pydantic import pydantic_model_creator
from app.models.user import User 

# 1. 요청 스키마 (UserInSchema로 통일)
class UserInSchema(BaseModel):
    username: str = Field(..., max_length=50)
    password: str = Field(..., min_length=8)
    email: str = Field(..., max_length=255)

# 2. 응답 스키마
UserOutSchema = pydantic_model_creator(
    User, 
    name="UserOutSchema", 
    exclude=("password_hash",) 
)

# 3. 토큰 응답 스키마
class TokenOutSchema(BaseModel):
    access_token: str
    token_type: str = "bearer"

# 🚨 만약 다른 파일에서 'UserIn'을 사용하고 있다면, 
# 'UserIn = UserInSchema'와 같이 별칭을 지정해주는 것도 방법입니다.