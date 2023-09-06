import base64
from io import BytesIO

from api.database import (add_user, get_user_photo, remove_user, retrieve_user,
                          retrieve_users, upload_user_photo)
from api.schemas.user import InputUser, UpdateUser
from fastapi import APIRouter, File, Form, HTTPException, UploadFile, status
from fastapi.responses import StreamingResponse

router = APIRouter()


@router.post("/create-user/")
async def create_user(user_data: InputUser):
    user = await add_user(user_data)
    return user


@router.get("/get-all-users/")
async def get_all_users():
    users = await retrieve_users()
    return users


@router.get("/get-user/{id}")
async def get_user(id):
    user = await retrieve_user(id)
    return user


@router.get("/get-user-photo/{id}")
async def get_photo(id):
    user_photo_bytes = await get_user_photo(id)
    if user_photo_bytes:
        print(type(user_photo_bytes))
        return StreamingResponse(BytesIO(user_photo_bytes), media_type="image/jpeg")
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {id} not found",
        )


@router.delete("/delete-user/{id}")
async def delete_user(id):
    try:
        await remove_user(id)
        return {"message": "User deleted successfully"}
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


@router.patch("/upload-photo/")
async def upload_photo(id: str = Form(...), photo: UploadFile = File(...)):
    binary_photo = await photo.read()
    user_data = UpdateUser(id=id, photo=binary_photo)
    user = await upload_user_photo(user_data)
    return user
