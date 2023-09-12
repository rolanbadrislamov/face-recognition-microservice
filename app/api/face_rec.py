import io

import numpy as np
from deepface import DeepFace
from PIL import Image

from app.api.database import get_all_profile_photos
from app.api.models.profile import ProfileOutput


async def verify(input_photo) -> ProfileOutput:
    all_photos = await get_all_profile_photos()

    input_image = Image.open(io.BytesIO(input_photo))

    input_ph = np.array(input_image)

    for profile in all_photos:
        photo = np.frombuffer(profile.photo, dtype=np.uint8)

        profile_image = Image.open(io.BytesIO(profile.photo))

        photo = np.array(profile_image)

        result = DeepFace.verify(input_ph, photo, model_name="Facenet")
        if result["verified"]:
            return ProfileOutput(**profile.dict())
        return {"message": "User not found"}
