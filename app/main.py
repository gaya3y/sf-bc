from fastapi import FastAPI
from app.users.endpoints import router as auth_router
from app.core.endpoints import router as core_router

app = FastAPI()
app.include_router(auth_router)
app.include_router(core_router)