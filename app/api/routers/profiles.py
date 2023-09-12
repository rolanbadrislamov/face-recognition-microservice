from io import BytesIO

from fastapi import (APIRouter, Depends, File, Form, HTTPException, UploadFile,
                     status)
from fastapi.responses import StreamingResponse

from app.api.database import (add_profile, get_profile_photo, remove_profile,
                              retrieve_profile, retrieve_profiles,
                              upload_profile_photo)
from app.api.dependencies import profile_credentials_exists, profile_exists
from app.api.face_rec import verify
from app.api.models.profile import ProfileInput, ProfilePhotoUpdate

router = APIRouter()


@router.post("/add-profile")
async def create_profile(profile_data: ProfileInput = Depends(profile_credentials_exists)):
    profile = await add_profile(profile_data)
    return profile


@router.get("/get-all-profiles")
async def get_all_profiles():
    users = await retrieve_profiles()
    return users


@router.get("/get-profile/{id}")
async def get_profile(id: str = Depends(profile_exists)):
    profile = await retrieve_profile(id)
    return profile


@router.get("/get-profile-photo/{id}")
async def get_photo(id: str = Depends(profile_exists)):
    profile_photo_bytes = await get_profile_photo(id)
    if type(profile_photo_bytes) == bytes:
        return StreamingResponse(BytesIO(profile_photo_bytes), media_type="image/jpeg")
    return profile_photo_bytes


@router.delete("/delete-profile/{id}")
async def delete_profile(id: str = Depends(profile_exists)):
    await remove_profile(id)
    return {"message": "Profile deleted successfully"}


@router.patch("/upload-profile-photo")
async def upload_photo(id: str = Form(...), photo: UploadFile = File(...), profile_exists=Depends(profile_exists)):
    binary_photo = await photo.read()
    profile_data = ProfilePhotoUpdate(id=id, photo=binary_photo)
    profile = await upload_profile_photo(profile_data)
    return profile


@router.post("/verify-profile")
async def verify_profile(input_photo: UploadFile = File(...)):
    input_photo_bytes = await input_photo.read()
    result = await verify(input_photo_bytes)
    return result


@router.patch("/update-profile")
async def update_profile(profile_data: ProfileInput = Depends(profile_credentials_exists)):
    pass
