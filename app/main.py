from fastapi import FastAPI

from app.api.routers.profiles import router as UserRouter
from app.config.settings import Settings

app = FastAPI()

try:
    Settings.validate()
except ValueError as e:
    print(f"Error: {e}")
app.include_router(UserRouter, tags=["Profiles"])


@app.get("/", tags=["ROOT"])
async def read_root():
    return {"msg": "This is a face recognition microservice. Please use the /docs endpoint to see the API documentation."}
