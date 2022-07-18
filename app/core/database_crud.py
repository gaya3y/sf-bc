from datetime import datetime
import logging
from app.core.models import Artist, Genre, ListeningHistory, Song

def create_listening_history_record(connecion, song_id, user_id):
    record = ListeningHistory(song_id=song_id, user_id=user_id)
    connecion.add(record)
    connecion.commit()
    connecion.refresh(record)
    return record   


def mark_end_of_song(connection, history):
    if history.end_time is not None:
        return history
    history.end_time = datetime.utcnow()
    connection.commit()
    connection.refresh(history)
    return history


def get_listening_history_of_user(connection, user_id, song_id=None, limit=None, offset=None):
    query = connection.query(ListeningHistory).filter(ListeningHistory.user_id == user_id)
    if song_id:
        query = query.filter(ListeningHistory.song_id == song_id)
    
    query = query.order_by(ListeningHistory.start_time.desc())

    if limit:
        query = query.limit(limit)
    if offset:
        query = query.offset(offset)

    return query.all()


def get_history_by_id(connection, history_id):
    return connection.query(ListeningHistory).get(history_id)


def get_songs_from_db(connection, limit=None, offset=None):
    query = connection.query(Song)
    if limit:
        query = query.limit(limit)
    if offset:
        query = query.offset(offset)
    return query.all()


def get_song_by_id(connection, song_id):
    return connection.query(Song).get(song_id)


def get_artists(connection, names):
    return connection.query(Artist).filter(Artist.name.in_(names)).all()


def get_genres(connection, names):
    return connection.query(Genre).filter(Genre.name.in_(names)).all()


def create_song(connnection, song):
    artists = get_artists(connnection, song.artists)
    genres = get_genres(connnection, song.genres)

    new_artists = [artist for artist in song.artists if artist not in artists]
    new_genres = [genre for genre in song.genres if genre not in genres]

    existing_artists = [artist for artist in artists if artist.name in song.artists]
    existing_genres = [genre for genre in genres if genre.name in song.genres]

    song_obj = Song(**song.dict(exclude={"artists", "genres"}))
    song_obj.artists.extend(existing_artists)
    song_obj.genres.extend(existing_genres)

    for artist in new_artists:
        new_artist = Artist(name=artist)
        connnection.add(new_artist)
        song_obj.artists.append(new_artist)
    
    for genre in new_genres:
        new_genre = Genre(name=genre)
        connnection.add(new_genre)
        song_obj.genres.append(new_genre)

    connnection.add(song_obj)
    connnection.commit()
    connnection.refresh(song_obj)
    logging.debug("Created song with (%d) new artists and (%d) new genres", len(new_artists), len(new_genres))
    return song_obj
