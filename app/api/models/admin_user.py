from pydantic import BaseModel, Field


class AdminUser(BaseModel):
    fullname: str = Field(...)
    username: str = Field(...)
    password: str = Field(...)


class AdminUserLogin(BaseModel):
    username: str = Field(...)
    password: str = Field(...)
