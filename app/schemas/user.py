from pydantic import BaseModel, Field

class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=32)
    password: str = Field(min_length=3, max_length=32)
    email: str = Field(max_length=255)

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        from_attributes = True
        orm_mode = True

class LoginResponse(BaseModel):
    access_token: str
    user: UserResponse
