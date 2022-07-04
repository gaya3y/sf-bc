from passlib.context import CryptContext
from app.settings import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY
from jose import JWTError, jwt
from datetime import datetime,timedelta

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(user_id):
    """
    Create a JWT Access Token with user_id
    """
    to_encode = {"sub": str(user_id)}
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_token(token):
    """
    Decode subject from JWT Token
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        return user_id
    except JWTError:
        return None



