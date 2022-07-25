from fastapi.security import OAuth2PasswordBearer
from os import environ

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")
SECRET_KEY = environ.get("SECRET_KEY", "a0236d0de85231cbbb7b8279926de4fc")

ALGORITHM = "HS256"

# 1 week default
ACCESS_TOKEN_EXPIRE_MINUTES = int(60 * 24 * 7)