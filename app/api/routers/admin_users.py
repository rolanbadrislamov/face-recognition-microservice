from fastapi import APIRouter, Body, Depends

from app.api.database import create_admin_user
from app.api.dependencies import check_admin
from app.api.models.admin_user import AdminUser, AdminUserLogin
from app.auth.auth_bearer import JWTBearer
from app.auth.auth_handler import signJWT

router = APIRouter()


@router.post("/signup")
async def create_admin(admin_data: AdminUser = Body(...)):
    created_admin = await create_admin_user(admin_data)
    return signJWT(created_admin.username)


@router.post("/login")
async def login_admin(admin_data: AdminUserLogin = Depends(check_admin)):
    return signJWT(admin_data["username"])
