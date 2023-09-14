from fastapi import FastAPI

from app.api.routers.profiles import router as ProfilesRouter

app = FastAPI()


app.include_router(ProfilesRouter, tags=["Profiles"])


@app.get("/", tags=["ROOT"])
async def read_root():
    return {"msg": "This is a face recognition microservice. Please use the /docs endpoint to see the API documentation."}
