from typing import List

import motor.motor_asyncio
from bson.objectid import ObjectId
from app.config.settings import (MONGODB_COLLECTION_NAME,
                             MONGODB_CONNECTION_STRING, MONGODB_DB_NAME)
from fastapi import HTTPException, status

from app.api.schemas.profile import (ProfileInput, ProfileOutput, ProfilePhotoInfo,
                              ProfileUpdate)

client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_CONNECTION_STRING)
database = client[MONGODB_DB_NAME]
user_collection = database[MONGODB_COLLECTION_NAME]


async def retrieve_profile(id: str) -> ProfileOutput:
    user = await user_collection.find_one({"_id": ObjectId(id)})
    if user:
        user = ProfileOutput(**user)
        return user
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User with id {id} not found",
    )


async def retrieve_profiles() -> List[ProfileOutput]:
    users = []
    async for user in user_collection.find():
        users.append(ProfileOutput(**user))
    return users


async def add_profile(user_data: ProfileInput) -> ProfileInput:
    result = await user_collection.insert_one(user_data.model_dump())
    created_user = await user_collection.find_one({"_id": result.inserted_id})
    created_user = ProfileOutput(**created_user)
    return created_user


async def remove_profile(id: str):
    try:
        await user_collection.delete_one({"_id": ObjectId(id)})
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {id} not found",
        )


async def upload_profile_photo(user_data: ProfileUpdate) -> ProfileOutput:
    updated_user = await user_collection.find_one_and_update(
        {"_id": ObjectId(user_data.id)},
        {"$set": {"photo": (
            user_data.photo), "updated_at": user_data.updated_at}},
    )
    if updated_user:
        return ProfileOutput(**updated_user)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User with id {id} not found",
    )


async def get_profile_photo(id: str) -> bytes:
    user = await user_collection.find_one({"_id": ObjectId(id)})
    return user["photo"]


async def get_all_profile_photos() -> List[ProfilePhotoInfo]:
    profiles = []
    async for profile_data in user_collection.find():
        if "photo" in profile_data:
            profile = ProfilePhotoInfo(**profile_data)
            profiles.append(profile)
    return profiles
