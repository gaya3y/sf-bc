from fastapi import APIRouter, Depends,HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app.database.dependency import get_db
from app.users.database_crud import add_user_connection, create_user, get_user_by_id, get_user_by_username, list_user, remove_user_connection
from app.users.datamodels import UserCreate, User
from app.users.auth import create_access_token,verify_password
from app.users.dependencies import get_current_user
from app.recommender.basic_recommender import BasicRecommender


router = APIRouter(
    prefix="/users"
)

@router.post("/create")
def signup(user: UserCreate, database_conn = Depends(get_db)):
    return User.from_orm(create_user(database_conn, user))

@router.get("/list")
def view(database_conn = Depends(get_db)):
    return [User.from_orm(user) for user in list_user(database_conn)]

@router.get("/me")
def me(current_user = Depends(get_current_user)):
    return User.from_orm(current_user)
 
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


@router.post("/connect/{user_id}")
def connect(user_id: str, database_conn = Depends(get_db),user = Depends(get_current_user)):
    target_user = get_user_by_id(database_conn, user_id)

    if target_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    if target_user.id == user.id:
        raise HTTPException(status_code=400, detail="You can't connect to yourself")

    add_user_connection(database_conn, user, target_user)


@router.delete("/connect/{user_id}")
def remove_connection(user_id: int, database_conn = Depends(get_db),user = Depends(get_current_user)):
    target_user = get_user_by_id(database_conn, user_id)

    if target_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    if target_user not in user.following:
        raise HTTPException(status_code=400, detail="You are not following this user")

    remove_user_connection(database_conn, user, target_user)


@router.get("/recommendations")
def recommendations(user = Depends(get_current_user), db_session = Depends(get_db)):
    return BasicRecommender.recommend_users(user_id=user.id, db_session=db_session)
