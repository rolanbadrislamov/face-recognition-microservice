import os

from dotenv import load_dotenv

load_dotenv()

mongo_host = os.getenv('MONGO_HOST', '')
mongo_port = int(os.getenv('MONGO_PORT', 27017))
MONGO_CONNECTION_STRING = f'mongodb://{mongo_host}:{mongo_port}'

MONGO_DB_NAME = "face-recognition"
MONGO_COLLECTION_NAME = "Person"
