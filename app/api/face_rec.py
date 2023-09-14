import io

import numpy as np
from deepface import DeepFace
from PIL import Image

from app.api.database import get_all_profile_photos
from app.api.models.profile import ProfileOutput


async def find_profile(input_image) -> ProfileOutput:
    all_photos = await get_all_profile_photos()

    input_image = Image.open(io.BytesIO(input_image))

    input_image_arr = np.array(input_image)

    for profile in all_photos:
        profile_image = Image.open(io.BytesIO(profile.photo))

        profile_image_arr = np.array(profile_image)

        result = DeepFace.verify(
            input_image_arr, profile_image_arr, model_name="Facenet")
        if result["verified"]:
            return ProfileOutput(**profile.model_dump())
    return {"message": "Profile not found"}
