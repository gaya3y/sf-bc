from multiprocessing.spawn import import_main_path
from sqlalchemy import Column, Integer, String
from app.database.connection import Base


class User(Base):
    __tablename__ = "users"

    username = Column("username", String, nullable=False, unique=True)
    password = Column("password", String,nullable = False)
    id = Column("id",Integer,nullable = False, primary_key = True)
    name = Column("name",String,nullable = False)