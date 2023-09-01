from api.models import Person
from api.crud import create_person
from fastapi import APIRouter

router = APIRouter()


@router.post("/create-user")
async def create_user(person: Person) -> dict:
    user = await create_person(person)
    return user
