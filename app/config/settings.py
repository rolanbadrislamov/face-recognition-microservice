import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    version = "0.1.0"
    title = "Face Recognition Microservice"

    app_settings = {
        'mongodb_host': os.getenv('MONGODB_HOST'),
        'mongodb_port': os.getenv('MONGODB_PORT'),
        'db_name': os.getenv('MONGODB_DB_NAME'),
        'db_username': os.getenv('MONGODB_USERNAME'),
        'db_password': os.getenv('MONGODB_PASSWORD'),
    }

    @classmethod
    def validate(cls):
        if not cls.app_settings['mongodb_host']:
            raise ValueError("MONGODB_HOST environment variable is not set.")
        if not cls.app_settings['mongodb_port']:
            raise ValueError("MONGODB_PORT environment variable is not set.")
        if not cls.app_settings['db_name']:
            raise ValueError("MONGO_DB_NAME environment variable is not set.")

    @classmethod
    def get_db_connection(cls):
        return f'mongodb://{cls.app_settings["mongodb_host"]}:{cls.app_settings["mongodb_port"]}'
