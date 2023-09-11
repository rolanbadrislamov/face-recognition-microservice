import json
from datetime import datetime
from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, EmailStr, Field


class ProfileBase(BaseModel):
    first_name: str = Field(min_length=1, max_length=128)
    last_name: str = Field(min_length=1, max_length=128)
    age: int = Field(gt=0, lt=150)
    phone_number: str = None
    email: Optional[EmailStr] = None


class ProfileInput(ProfileBase):
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class ProfileOutput(ProfileInput):
    id: ObjectId = Field(alias="_id")

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class ProfileUpdate(BaseModel):
    id: str
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    photo: bytes

    class Config:
        arbitrary_types_allowed = True


class ProfilePhotoInfo(ProfileOutput):
    photo: bytes

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
