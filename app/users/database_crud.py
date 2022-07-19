from app.users.models import User
from app.users.auth import get_password_hash


def create_user(connection, user_data):
    user_obj = User(**user_data.dict())
    user_obj.password = get_password_hash(user_obj.password)
    connection.add(user_obj)
    connection.commit()
    connection.refresh(user_obj)
    return user_obj

def list_user(connection, limit = None, offset = None):
    query = connection.query(User)
    if limit:
        query = query.limit(limit)
    if offset:
        query = query.offset(limit * offset)
    return query.all()

def get_user_by_username(connection,username):
    return connection.query(User).filter(User.username == username).first()

def get_user_by_id(connection,userid):
    return connection.query(User).filter(User.id == userid).first()

def add_user_connection(db_conn, user, following):
    user.following.append(following)
    db_conn.commit()

def remove_user_connection(db_conn, user, following):
    user.following.remove(following)
    db_conn.commit()
