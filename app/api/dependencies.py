import io

import motor.motor_asyncio
from bson import ObjectId
from fastapi import HTTPException, UploadFile, status
from PIL import Image

from app.api.models.profile import ProfileInput, ProfileUpdate
from app.config.settings import Settings

client = motor.motor_asyncio.AsyncIOMotorClient(
    Settings.get_db_connection())
database = client[Settings.app_settings["db_name"]]
profiles_collection = database["profiles"]


async def profile_credentials_exists(profile_data: ProfileInput):
    profile = await profiles_collection.find_one({"$or": [{"email": profile_data.email}, {"phone_number": profile_data.phone_number}]})
    if profile:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Profile with this email or phone number already exists",
        )
    return profile_data


async def profile_credentials_update(id, profile_data: ProfileUpdate):
    profile = await profiles_collection.find_one({
        "$or": [
            {"email": profile_data.email, "_id": {"$ne": ObjectId(id)}},
            {"phone_number": profile_data.phone_number,
                "_id": {"$ne": ObjectId(id)}},
        ]
    })

    if profile:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Profile with this email or phone number already exists",
        )

    return profile_data


async def profile_exists(id: str):
    profile = await profiles_collection.find_one({"_id": ObjectId(id)})
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Profile with id {id} not found",
        )
    return id


async def verify_photo(photo: UploadFile):
    try:
        photo_data = await photo.read()
        with Image.open(io.BytesIO(photo_data)) as img:
            valid_formats = ('JPEG', 'PNG', 'GIF')
            if img.format not in valid_formats:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Unsupported image format. Please upload a valid photo.",
                )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Photo verification failed. Check if it is a valid photo.",
        )
    return photo_data
