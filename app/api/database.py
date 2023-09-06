from datetime import datetime
from typing import List

import motor.motor_asyncio
from bson import Binary
from bson.objectid import ObjectId
from config.settings import (MONGODB_COLLECTION_NAME,
                             MONGODB_CONNECTION_STRING, MONGODB_DB_NAME)
from fastapi import HTTPException, status

from .schemas.user import InputUser, OutputUser, UpdateUser

client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_CONNECTION_STRING)
database = client[MONGODB_DB_NAME]
user_collection = database[MONGODB_COLLECTION_NAME]


async def retrieve_user(id: str) -> OutputUser:
    user = await user_collection.find_one({"_id": ObjectId(id)})
    if user:
        user = OutputUser(**user)
        return user
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User with id {id} not found",
    )


async def retrieve_users() -> List[OutputUser]:
    users = []
    async for user in user_collection.find():
        users.append(OutputUser(**user))
    return users


async def add_user(user_data: InputUser) -> OutputUser:
    result = await user_collection.insert_one(user_data.model_dump())
    created_user = await user_collection.find_one({"_id": result.inserted_id})
    created_user = OutputUser(**created_user)
    return created_user


async def remove_user(id: str):
    try:
        await user_collection.delete_one({"_id": ObjectId(id)})
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {id} not found",
        )


async def upload_user_photo(user_data: UpdateUser) -> OutputUser:
    updated_user = await user_collection.find_one_and_update(
        {"_id": ObjectId(user_data.id)},
        {"$set": {"photo": (
            user_data.photo), "updated_at": user_data.updated_at}},
    )
    if updated_user:
        return OutputUser(**updated_user)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User with id {id} not found",
    )


async def get_user_photo(id: str) -> bytes:
    user = await user_collection.find_one({"_id": ObjectId(id)})
    return user["photo"]
