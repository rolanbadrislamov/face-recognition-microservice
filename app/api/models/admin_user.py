from pydantic import BaseModel, Field
from pydantic import BaseModel, EmailStr

class AdminUser(BaseModel):
    email: EmailStr = Field(...)
    username: str = Field(...)
    password: str = Field(...)


class AdminUserLogin(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(...)
