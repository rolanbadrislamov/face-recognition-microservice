from api.crud import retrieve_people, retrieve_person
from fastapi import APIRouter

router = APIRouter()


@router.get("/get-all-users")
async def get_all_users():
    users = await retrieve_people()
    return users


@router.get("/get-user")
async def get_user(id):
    user = await retrieve_person(id)
    return user
