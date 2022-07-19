from sqlalchemy import ForeignKey, Integer, Column, DateTime, Table, func, String
from sqlalchemy.orm import relationship
from app.database.connection import Base, metadata_obj


class ListeningHistory(Base):
    __tablename__ = "listening_history"

    id = Column("id", Integer, primary_key=True)
    user_id = Column("user_id", Integer, ForeignKey("users.id"), nullable=False)
    song_id = Column("song_id", Integer, ForeignKey("songs.id"), nullable=False)
    start_time = Column("start_time", DateTime, nullable=False, server_default=func.now())
    end_time =  Column("end_time", DateTime)

    song = relationship("Song")
    user = relationship("User")


class Artist(Base):
    __tablename__ = "artists"

    id = Column("id", Integer, primary_key=True)
    name = Column("name", String, nullable=False)


class Genre(Base):
    __tablename__ = "genres"

    id = Column("id", Integer, primary_key=True)
    name = Column("name", String, nullable=False)

song_artist_table = Table(
    "song_has_artist",
    metadata_obj,
    Column("song_id", Integer, primary_key=True),
    Column("artist_id", Integer, ForeignKey(Artist.id), primary_key=True)
)

song_genre_table = Table(
    "song_has_genre",
    metadata_obj,
    Column("song_id", Integer, primary_key=True),
    Column("genre_id", Integer, ForeignKey(Genre.id), primary_key=True)
)

class Song(Base):
    __tablename__ = "songs"

    id = Column("id", Integer, primary_key=True)
    name = Column("name", String, nullable=False)
    duration = Column("duration", Integer, nullable=False)
    url = Column("url", String, nullable=False)

    artists = relationship(
        "Artist",
        secondary=song_artist_table,
        backref="songs",
        primaryjoin= song_artist_table.c.song_id == id,
        secondaryjoin= song_artist_table.c.artist_id == Artist.id
    )
    genres = relationship(
        "Genre",
        secondary=song_genre_table,
        backref="songs",
        primaryjoin=id == song_genre_table.c.song_id,
        secondaryjoin=Genre.id == song_genre_table.c.genre_id
    )
