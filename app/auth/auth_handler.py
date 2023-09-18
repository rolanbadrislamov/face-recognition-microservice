import time

import jwt

from app.config.settings import settings

JWT_SECRET = settings.SECRET_KEY
JWT_ALGORITHM = settings.ALGORITHM


def token_response(token: str):
    return {
        "access_token": token,
    }


def signJWT(user_id: str) -> dict[str, str]:
    payload = {
        "user_id": user_id,
        "expires": time.time() + 600
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return token_response(token)


def decodeJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(
            token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except Exception as e:
        return {"error": "Invalid token", "details": e}
