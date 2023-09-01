from api.endpoints.get import router as get_router
from api.endpoints.upload import router as upload_router
from api.endpoints.delete import router as delete_router
from fastapi import FastAPI

app = FastAPI()
app.include_router(get_router)
app.include_router(upload_router)
app.include_router(delete_router)
