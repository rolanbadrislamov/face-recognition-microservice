import io

import motor.motor_asyncio
from bson import ObjectId
from fastapi import HTTPException, UploadFile, status
from PIL import Image

from app.api.models.admin_user import AdminUserLogin
from app.api.models.profile import ProfileInput, ProfileUpdate
from app.auth.auth_bearer import verify_password
from app.config.settings import settings

client = motor.motor_asyncio.AsyncIOMotorClient(
    settings.MONGODB_CONN_STRING)
database = client[settings.MONGODB_DB]
profiles_collection = database[settings.PROFILES_COLLECTION]
admin_users_collection = database[settings.ADMIN_USERS_COLLECTION]


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
    try:
        profile_id = ObjectId(id)
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid profile id",
        )
    profile = await profiles_collection.find_one({"_id": profile_id})
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


async def check_admin(admin_data: AdminUserLogin):
    admin = await admin_users_collection.find_one({"email": admin_data.email})
    if not admin or not verify_password(admin_data.password, admin["password"]):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Admin user not found",
        )
    return admin
