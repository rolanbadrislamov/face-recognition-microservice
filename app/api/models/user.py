from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    name: str = Field(min_length=1, max_length=128)
    age: int = Field(gt=0, lt=150)
    phone_number: Optional[str] = None
    email: Optional[EmailStr] = None


class CreateUser(UserBase):
    photo: bytes
