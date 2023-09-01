from api.crud import delete_person
from fastapi import APIRouter

router = APIRouter()


@router.delete("/delete-user")
async def delete_user(id):
    await delete_person(id)
    return {"message": "User deleted successfully"}
