from datetime import datetime
from datetime import timedelta
from sqlalchemy import distinct, func, text
from app.core.models import Artist, Genre, ListeningHistory, Song

def db_get_favorite_songs(db_connection, user_id):
    query = db_connection.query(
        ListeningHistory.song_id,
        func.sum(ListeningHistory.end_time - ListeningHistory.start_time
    ).label("duration"))\
        .filter(ListeningHistory.user_id==user_id, ListeningHistory.end_time != None)\
    
    recent_query = \
        query.filter(ListeningHistory.start_time >= datetime.utcnow() - timedelta(days=30))

    raw = recent_query.group_by(ListeningHistory.song_id)\
        .order_by(text("duration desc"))\
        .limit(10)\
        .all()
    
    if len(raw) < 5:
        raw = query.group_by(ListeningHistory.song_id)\
        .order_by(text("duration desc"))\
        .limit(10)\
        .all()
    
    return [{"song_id": r[0], "duration": r[1]}  for r in raw]


def _get_popular_songs_by_category(db_connection, filter, excluded_songs, limit):
    query = db_connection.query(
        distinct(Song.id).label("song_id"),
        func.sum(ListeningHistory.end_time - ListeningHistory.start_time).label("duration")
    )\
        .select_from(Song)\
        .join(ListeningHistory, Song.id == ListeningHistory.song_id)\
        .filter(filter, Song.id.not_in(excluded_songs))\
        .filter(ListeningHistory.end_time != None)\
        .group_by(Song.id)\
        .order_by(text("duration desc"))\
        .limit(limit)\
        .all()

    return [{"song_id": r[0], "duration": r[1]}  for r in query]


def get_popular_songs_by_artist(db_connection, artist_id, excluded_songs, limit):
    return _get_popular_songs_by_category(db_connection, Song.artists.any(Artist.id == artist_id), excluded_songs, limit)


def db_get_popular_songs_by_genre(db_connection, genre_id, excluded_songs, limit):
    return _get_popular_songs_by_category(db_connection, Song.genres.any(Genre.id == genre_id), excluded_songs, limit)
