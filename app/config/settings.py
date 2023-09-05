import os

from dotenv import load_dotenv

load_dotenv()

mongo_host = os.getenv('MONGODB_HOST', '')
mongo_port = int(os.getenv('MONGODB_PORT', 27017))
MONGODB_CONNECTION_STRING = f'mongodb://{mongo_host}:{mongo_port}'

MONGODB_DB_NAME = os.getenv("MONGODB_DB_NAME", "face-recognition")
MONGODB_COLLECTION_NAME = os.getenv("MONGODB_COLLECTION_NAME", "people")
