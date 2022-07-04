from sqlalchemy import Integer, Column, DateTime, func, String
from app.database.connection import Base


class ListeningHistory(Base):
    __tablename__ = "listening_history"

    id = Column("id", Integer, primary_key=True)
    user_id = Column("user_id", Integer, nullable=False)
    song_id = Column("song_id", Integer, nullable=False)
    start_time = Column("start_time", DateTime, nullable=False, server_default=func.now())
    end_time =  Column("end_time", DateTime, nullable=False)


class Song(Base):
    __tablename__ = "songs"

    id = Column("id", Integer, primary_key=True)
    name = Column("name", String, nullable=False)
    duration = Column("duration", Integer, nullable=False)
    url = Column("url", String, nullable=False)
