from bson.objectid import ObjectId
from fastapi import HTTPException, status

from .database import person_collection
from .models import Person


async def retrieve_person(id: str) -> dict:
    try:
        person = await person_collection.find_one({"_id": ObjectId(id)})
        person["_id"] = str(person["_id"])
        return person
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Person with id {id} not found",
        )


async def retrieve_people() -> dict:
    people = []
    async for person in person_collection.find():
        person["_id"] = str(person["_id"])
        people.append(person)
    return people


async def create_person(person: Person) -> dict:
    result = await person_collection.insert_one(person.dict())
    created_person = await person_collection.find_one({"_id": result.inserted_id})
    return str(created_person["_id"])


async def delete_person(id: str):
    try:
        await person_collection.delete_one({"_id": ObjectId(id)})
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Person with id {id} not found",
        )
