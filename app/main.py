from fastapi import FastAPI
from app.users.endpoints import router

app = FastAPI()
app.include_router(router)