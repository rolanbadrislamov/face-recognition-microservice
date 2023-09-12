import motor.motor_asyncio
from bson import ObjectId
from fastapi import Depends, HTTPException, status

from app.api.models.profile import ProfileInput
from app.config.settings import Settings

client = motor.motor_asyncio.AsyncIOMotorClient(
    Settings.get_db_connection())
database = client[Settings.app_settings["db_name"]]
profiles_collection = database["profiles"]


async def profile_credentials_exists(ProfileData: ProfileInput):
    profile = await profiles_collection.find_one({"$or": [{"email": ProfileData.email}, {"phone_number": ProfileData.phone_number}]})
    if profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile with this email or phone number already exists",
        )
    return ProfileData


async def profile_exists(id: str):
    profile = await profiles_collection.find_one({"_id": ObjectId(id)})
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {id} not found",
        )
    return id
