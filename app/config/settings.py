import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    version = "0.1.0"
    title = "Face Recognition Microservice"

    MONGODB_HOST: str = os.environ.get('MONGODB_HOST')
    MONGODB_PORT: str = os.environ.get('MONGODB_PORT')
    MONGODB_USER: str = os.environ.get('MONGODB_USER')
    MONGODB_PASSWORD: str = os.environ.get('MONGODB_PASSWORD')
    MONGODB_DB: str = os.environ.get('MONGODB_DB')
    MONGODB_CONN_STRING: str = (
        f"mongodb://{MONGODB_USER}:{MONGODB_PASSWORD}@{MONGODB_HOST}:{MONGODB_PORT}"
    )

    PROFILES_COLLECTION = 'profiles'
    ADMIN_USERS_COLLECTION = 'admin_users'

    SECRET_KEY: str = os.environ.get('SECRET_KEY')
    ALGORITHM = "HS256"


settings = Settings()
