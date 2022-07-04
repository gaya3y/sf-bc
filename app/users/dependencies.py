from fastapi import Depends, HTTPException
from app.database.dependency import get_db
from app.users.auth import decode_token
from app.settings import oauth2_scheme
from app.users.database_crud import get_user_by_id

def get_current_user(database = Depends(get_db), token = Depends(oauth2_scheme)):
    user_id = decode_token(token)
    error = HTTPException(
        status_code=401,
        detail="Not authenticated"
    )
    if user_id is None:
        raise error
    user = get_user_by_id(database, user_id)
    if user is None:
        raise error
    return user
