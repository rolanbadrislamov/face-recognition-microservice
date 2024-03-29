from io import BytesIO

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from fastapi.responses import StreamingResponse

from app.api.database import (add_profile, get_profile_photo, modify_profile,
                              remove_profile, retrieve_profile,
                              retrieve_profiles, upload_profile_photo)
from app.api.dependencies import (profile_credentials_exists,
                                  profile_credentials_update, profile_exists,
                                  verify_photo)
from app.api.face_rec import find_profile
from app.api.models.profile import (ProfileInput, ProfilePhotoUpdate,
                                    ProfileUpdate)
from app.auth.auth_bearer import JWTBearer

router = APIRouter()


@router.post("/add-profile")
async def create_profile(profile_data: ProfileInput = Depends(profile_credentials_exists), token: str = Depends(JWTBearer())):
    profile = await add_profile(profile_data)
    return profile


@router.get("/all-profiles")
async def get_all_profiles(token: str = Depends(JWTBearer())):
    users = await retrieve_profiles()
    return users


@router.get("/profile/{id}")
async def get_profile(id: str = Depends(profile_exists), token: str = Depends(JWTBearer())):
    try:
        profile = await retrieve_profile(id)
        return profile
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Photo of profile:{id} not found"
        )


@router.get("/profile-photo/{id}")
async def get_photo(id: str = Depends(profile_exists), token: str = Depends(JWTBearer())):
    profile_photo_bytes = await get_profile_photo(id)
    if type(profile_photo_bytes) == bytes:
        return StreamingResponse(BytesIO(profile_photo_bytes), media_type="image/jpeg")
    return profile_photo_bytes


@router.delete("/profile/{id}")
async def delete_profile(id: str = Depends(profile_exists), token: str = Depends(JWTBearer())):
    await remove_profile(id)
    return {"message": "Profile deleted successfully"}


@router.patch("/profile-photo{id}")
async def upload_photo(id: str, photo: UploadFile = File(...), token: str = Depends(JWTBearer())):
    await profile_exists(id)
    photo = await verify_photo(photo)
    profile_data = ProfilePhotoUpdate(
        id=id, photo=photo)
    await upload_profile_photo(profile_data)
    return {"message": "Profile photo updated successfully"}


@router.post("/verify-profile")
async def verify_profile(photo: UploadFile = Depends(verify_photo), token: str = Depends(JWTBearer())):
    try:
        result = await find_profile(photo)
        if result:
            return result
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Profile not found. Please confirm that the picture is a face photo"
        )


@router.patch("/profile{id}")
async def update_profile(profile_data: ProfileUpdate, id: str = Depends(profile_exists), token: str = Depends(JWTBearer())):
    await profile_credentials_update(id=id, profile_data=profile_data)
    profile = await modify_profile(id, profile_data)
    return profile
