from datetime import datetime
from typing import List, Optional

from bson import Binary
from pydantic import BaseModel, EmailStr


class Person(BaseModel):
    name: str
    last_name: str
    age: int
    job_title: Optional[str] = None
    phone_number: str
    email: Optional[EmailStr] = None
    photo: bytes

    class Config:
        default = {
            "date_registered": datetime.now()
        }
        schema_extra = {
            "example": {
                "name": "John",
                "last_name": "Doe",
                "age": 30,
                "job_title": "Software Engineer",
                "phone_number": "1234567890",
                "email": "johndoe@example.com",
                "photo": b"binary_data_here"
            }
        }
        arbitrary_types_allowed = True
