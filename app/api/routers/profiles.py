import time
from io import BytesIO

from fastapi import APIRouter, File, Form, HTTPException, UploadFile, status
from fastapi.responses import StreamingResponse

from app.api.database import (add_profile, get_all_profile_photos,
                              get_profile_photo, remove_profile,
                              retrieve_profile, retrieve_profiles,
                              upload_profile_photo)
from app.api.face_rec import verify
from app.api.schemas.profile import ProfileInput, ProfileUpdate

router = APIRouter()


@router.post("/add-profile/")
async def create_profile(user_data: ProfileInput):
    user = await add_profile(user_data)
    return user


@router.get("/get-all-profiles/")
async def get_all_profiles():
    users = await retrieve_profiles()
    return users


@router.get("/get-profile/{id}")
async def get_profile(id):
    user = await retrieve_profile(id)
    return user


@router.get("/get-profile-photo/{id}")
async def get_photo(id):
    user_photo_bytes = await get_profile_photo(id)
    if user_photo_bytes:
        print(type(user_photo_bytes))
        return StreamingResponse(BytesIO(user_photo_bytes), media_type="image/jpeg")
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {id} not found",
        )


@router.delete("/delete-profile/{id}")
async def delete_profile(id):
    try:
        await remove_profile(id)
        return {"message": "User deleted successfully"}
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


@router.patch("/upload-photo/")
async def upload_photo(id: str = Form(...), photo: UploadFile = File(...)):
    binary_photo = await photo.read()
    user_data = ProfileUpdate(id=id, photo=binary_photo)
    user = await upload_profile_photo(user_data)
    return user


@router.post("/verify-profile/")
async def verify_profile(input_photo: UploadFile = File(...)):
    input_photo_bytes = await input_photo.read()
    result = await verify(input_photo_bytes)
    return result
