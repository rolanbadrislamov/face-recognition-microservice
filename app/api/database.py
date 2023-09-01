import os

import motor.motor_asyncio
from config.settings import (MONGO_COLLECTION_NAME, MONGO_CONNECTION_STRING,
                             MONGO_DB_NAME)

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_CONNECTION_STRING)
database = client[MONGO_DB_NAME]
person_collection = database[MONGO_COLLECTION_NAME]
