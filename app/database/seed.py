from datetime import datetime, timedelta
import os

from random import choice, sample
from faker import Faker
from app.core.database_crud import create_listening_history_record, create_song, get_genres
from app.database.connection import verify_postgres
from app.users.datamodels import UserCreate
from app.core.datamodels import SongCreate
from app.core.models import Artist, Genre, ListeningHistory, Song
from app.users.models import User
from app.database.dependency import get_db
from app.users.database_crud import create_user


fake = Faker()


def create_artists(db_session):
    artists = [fake.name() for _ in range(10)]
    artists_obj = set(Artist(name=artist) for artist in artists)
    db_session.add_all(artists_obj)
    return artists


def create_genres(db_session):
    genres = ("rock", "pop", "hip hop", "jazz", "country", "soul", "classical", "reggae", "metal")
    genre_objs = {Genre(name=genre) for genre in genres}
    existing = set(get_genres(db_session, genres))
    db_session.add_all(genre_objs - existing)
    db_session.commit()
    return genres


def create_listening_history(db_session, users, songs):
    for user in users:
        listened_songs = sample(songs, fake.random_int(3, 10))
        for song in listened_songs:
            create_listening_history_record(
                db_session,
                song.id,
                user.id,
                datetime.utcnow() + timedelta(seconds=fake.random_int(4, song.duration))
            )



def main():
    verify_postgres()
    users = []
    db_session = next(get_db())
    artists = []
    password = "password"
    for _ in range(5):
        users.append(create_user(
            db_session,
            UserCreate(
                username=fake.email(),
                name=fake.name(),
                password=password
            )
        ))
    artists = create_artists(db_session)
    genres = create_genres(db_session)
    songs = [
        create_song(
            db_session,
            SongCreate(
                name=fake.name(),
                artists=choice([sample(artists, 2), [choice(artists)]]),
                genres=choice([sample(genres, fake.random_int(2, 3)), [choice(genres)]]),
                duration=fake.random_int(120, 240),
                url=fake.url()
            )
        )
    for _ in range(50)]
    create_listening_history(db_session, users, songs)


if __name__ == "__main__":
    main()