from fastapi import FastAPI

from app.api.routers.admin_users import router as AdminUsersRouter
from app.api.routers.profiles import router as ProfilesRouter

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(ProfilesRouter, tags=["Profiles"], prefix="/profiles")
app.include_router(AdminUsersRouter, tags=[
                   "Admin Users"], prefix="/admins")


@app.get("/", tags=["ROOT"])
async def read_root():
    return {"msg": "This is a face recognition microservice. Please use the /docs endpoint to see the API documentation."}
