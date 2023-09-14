import re
from datetime import datetime
from typing import Optional

from bson import ObjectId
from pydantic import AliasChoices, BaseModel, EmailStr, Field, validator


class ProfileBase(BaseModel):
    first_name: str = Field(min_length=1, max_length=128)
    last_name: str = Field(min_length=1, max_length=128)
    age: int = Field(gt=0, lt=150)
    phone_number: str
    email: Optional[EmailStr] = None

    @validator('phone_number')
    def validate_phone_number(cls, phone_number):
        phone_number_pattern = r'^\+\d{1,3}\s?\d{1,14}$'

        if not re.match(phone_number_pattern, phone_number):
            raise ValueError("Invalid phone number format")

        return phone_number

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class ProfileInput(ProfileBase):
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class ProfileOutput(ProfileInput):
    id: ObjectId = Field(validation_alias=AliasChoices('_id', 'id'))


class ProfileUpdate(ProfileBase):
    first_name: Optional[str] = Field(
        min_length=1, max_length=128, default=None)
    last_name: Optional[str] = Field(
        min_length=1, max_length=128, default=None)
    age: Optional[int] = Field(gt=0, lt=150, default=None)
    phone_number: Optional[str] = None
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class ProfilePhotoUpdate(BaseModel):
    id: str
    photo: bytes
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class ProfilePhotoInfo(ProfileOutput):
    photo: bytes
