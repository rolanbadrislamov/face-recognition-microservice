from api.routers.users import router as UserRouter
from fastapi import FastAPI

app = FastAPI()

app.include_router(UserRouter, tags=["User"])


@app.get("/", tags=["ROOT"])
async def read_root():
    return {"msg": "This is a face recognition microservice. Please use the /docs endpoint to see the API documentation."}
