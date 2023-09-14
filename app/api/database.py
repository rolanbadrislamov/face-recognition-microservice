from typing import List

import motor.motor_asyncio
from bson.objectid import ObjectId

from app.api.models.profile import (ProfileInput, ProfileOutput,
                                    ProfilePhotoInfo, ProfilePhotoUpdate,
                                    ProfileUpdate)
from app.config.settings import Settings

client = motor.motor_asyncio.AsyncIOMotorClient(
    Settings.get_db_connection())
database = client[Settings.app_settings["db_name"]]
profiles_collection = database["profiles"]


async def retrieve_profile(id: str) -> ProfileOutput:
    profile = await profiles_collection.find_one({"_id": ObjectId(id)})
    if profile:
        profile = ProfileOutput(**profile)
        return profile


async def retrieve_profiles() -> List[ProfileOutput]:
    profiles = []
    async for profile in profiles_collection.find():
        profiles.append(ProfileOutput(**profile))
    return profiles


async def add_profile(profile_data: ProfileInput) -> ProfileInput:
    result = await profiles_collection.insert_one(profile_data.model_dump())
    created_profile = await profiles_collection.find_one({"_id": result.inserted_id})
    created_profile = ProfileOutput(**created_profile)
    return created_profile


async def remove_profile(id: str):
    await profiles_collection.delete_one({"_id": ObjectId(id)})
    return {"message": "Profile deleted successfully"}


async def upload_profile_photo(profile_data: ProfilePhotoUpdate) -> ProfileOutput:
    updated_profile = await profiles_collection.find_one_and_update(
        {"_id": ObjectId(profile_data.id)},
        {"$set": {"photo": (
            profile_data.photo), "updated_at": profile_data.updated_at}},
    )
    if updated_profile:
        return
    else:
        raise Exception(
            f"Profile with id {profile_data.id} could not be updated")


async def get_profile_photo(id: str) -> bytes:
    profile = await profiles_collection.find_one({"_id": ObjectId(id)})
    if "photo" in profile:
        return profile["photo"]
    else:
        return {"message": "Profile photo not found"}


async def get_all_profile_photos() -> List[ProfilePhotoInfo]:
    profiles = []
    async for profile_data in profiles_collection.find():
        if "photo" in profile_data:
            profile = ProfilePhotoInfo(**profile_data)
            profiles.append(profile)
    return profiles


async def modify_profile(id, profile_data: ProfileUpdate) -> ProfileOutput:
    profile = profile_data.model_dump(exclude_unset=True)
    updated_profile = await profiles_collection.find_one_and_update(
        {"_id": ObjectId(id)},
        {"$set": profile},
        return_document=True
    )
    return ProfileOutput(**updated_profile)
