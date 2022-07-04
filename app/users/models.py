from sqlalchemy import Column, Integer, String, Boolean, Table
from sqlalchemy.orm import relationship
from app.database.connection import Base, metadata_obj


user_circle = Table("user_circle", metadata_obj,
    Column("following_id", Integer, primary_key=True),
    Column("user_id", Integer, primary_key=True),
    Column("is_compatible", Boolean, nullable=False, default=False)
)


class User(Base):
    __tablename__ = "users"

    username = Column("username", String, nullable=False, unique=True)
    password = Column("password", String,nullable = False)
    id = Column("id",Integer,nullable = False, primary_key = True)
    name = Column("name",String,nullable = False)

    followers = relationship(
        "User",
        secondary=user_circle,
        primaryjoin=user_circle.c.following_id == id,
        secondaryjoin=user_circle.c.user_id == id,
        backref="following",
    )
