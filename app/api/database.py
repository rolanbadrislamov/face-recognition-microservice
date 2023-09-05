from typing import List

import motor.motor_asyncio
from bson import Binary
from bson.objectid import ObjectId
from config.settings import (MONGODB_COLLECTION_NAME, MONGODB_CONNECTION_STRING,
                             MONGODB_DB_NAME)
from fastapi import HTTPException, status
from .models.user import UserBase, CreateUser


client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_CONNECTION_STRING)
database = client[MONGO_DB_NAME]
user_collection = database[MONGO_COLLECTION_NAME]


async def retrieve_user(id: str) -> UserBase:
    user = await user_collection.find_one({"_id": ObjectId(id)})
    if user:
        user = UserBase(**user)
        return user
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User with id {id} not found",
    )


async def retrieve_users() -> List[UserBase]:
    users = []
    async for user in user_collection.find():
        users.append(UserBase(**user))
    return users


async def upload_user(userdata: CreateUser) -> dict:

    result = await user_collection.insert_one(userdata)
    created_user = await user_collection.find_one({"_id": result.inserted_id})
    created_user = UserBase(**created_user)
    return created_user


async def remove_user(id: str):
    try:
        await user_collection.delete_one({"_id": ObjectId(id)})
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {id} not found",
        )
