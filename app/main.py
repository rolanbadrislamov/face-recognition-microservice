from app.api.routers.profiles import router as UserRouter
from fastapi import FastAPI

app = FastAPI()

app.include_router(UserRouter, tags=["Profiles"])


@app.get("/", tags=["ROOT"])
async def read_root():
    return {"msg": "This is a face recognition microservice. Please use the /docs endpoint to see the API documentation."}
