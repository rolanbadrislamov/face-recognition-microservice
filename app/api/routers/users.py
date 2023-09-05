from api.database import (remove_user, retrieve_user, retrieve_users,
                          upload_user)
from api.models.user import CreateUser, UserBase
from fastapi import APIRouter, Body, File, UploadFile

router = APIRouter()


@router.post("/create-user")
async def create_user(userdata: UserBase = Body(...), photo: UploadFile = File(...)):

    binary_photo = photo.file.read()
    user = CreateUser(**userdata.model_dump(), photo=binary_photo)
    return user


@router.get("/get-all-users")
async def get_all_users():
    users = await retrieve_users()
    return users


@router.get("/get-user{id}")
async def get_user(id):
    user = await retrieve_user(id)
    return user


@router.get("/get-user-photo/{id}")
async def get_photo(id):
    user = await retrieve_user(id)
    return user["photo"]


router = APIRouter()


@router.delete("/delete-user")
async def delete_user(id):
    await remove_user(id)
    return {"message": "User deleted successfully"}
