from fastapi import APIRouter, Depends,HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app.database.dependency import get_db
from app.users.database_crud import create_user, get_user_by_username, list_user
from app.users.datamodels import UserCreate
from app.settings import oauth2_scheme
from app.users.auth import create_access_token,verify_password
from app.users.dependencies import get_current_user


router = APIRouter(
    prefix="/users"
)

@router.post("/create")
def signup(user: UserCreate, database_conn = Depends(get_db)):
    return create_user(database_conn, user)

@router.get("/list")
def view( database_conn = Depends(get_db),user = Depends(get_current_user)):
    print(user.username)
    return list_user(database_conn)
 
@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), database_conn = Depends(get_db)):
    user_in_db = get_user_by_username(database_conn,form_data.username)

    error = HTTPException(
        status_code=401,
        detail="Not authenticated")

    if user_in_db is None:
        raise error
    if verify_password(form_data.password, user_in_db.password):
        return {"access_token": create_access_token(user_in_db.id), "token_type": "Bearer"}

        
    raise error


