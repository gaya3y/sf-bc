from typing import List
from fastapi import APIRouter, Depends
from app.core.database_crud import create_listening_history_record, create_song, get_listening_history_of_user, get_songs_from_db, mark_end_of_song
from app.core.datamodels import ListeningHistory, Song, SongCreate
from app.core.dependencies import get_history_or_404, get_song_or_404
from app.recommender.basic_recommender import BasicRecommender
from app.recommender.db_crud import db_get_favorite_songs
from app.users.dependencies import get_current_user
from app.database.dependency import get_db

router = APIRouter(
    prefix=""
)

@router.post("/history")
def listen_to_song(
    song = Depends(get_song_or_404),
    database_conn = Depends(get_db),
    user = Depends(get_current_user)
):
    return create_listening_history_record(database_conn, song.id, user.id)

@router.patch("/history/{history_id}")
def mark_song_ended(
    history = Depends(get_history_or_404),
    database_conn = Depends(get_db),    
):
    return mark_end_of_song(database_conn, history)


@router.get("/history", response_model=List[ListeningHistory])
def get_listening_history(
    limit: int = 100,
    offset: int = 0,
    database_conn = Depends(get_db),
    user = Depends(get_current_user),
):
    data = get_listening_history_of_user(database_conn, user.id, limit=limit, offset=offset)
    return [ListeningHistory.from_orm(history) for history in data]


@router.get("/songs")
def get_songs(
    limit: int = 100,
    offset: int = 0,
    q: str = None,
    database_conn = Depends(get_db),
):
    return [Song.from_orm(song) for song in get_songs_from_db(database_conn, limit=limit, offset=offset, q=q)]


@router.post("/songs", dependencies=[Depends(get_current_user)])
def new_song(song: SongCreate, database_conn = Depends(get_db)):
    return create_song(database_conn, song)


@router.get("/songs/recommendations")
def recommended_songs(db_session = Depends(get_db), current_user = Depends(get_current_user)):
    return BasicRecommender.recommend_songs(db_session, current_user.id)

@router.get("/songs/favorite")
def get_favourite_songs(db_session = Depends(get_db), current_user = Depends(get_current_user)):
    song_ids = [i["song_id"] for i in db_get_favorite_songs(db_session, current_user.id)]
    return [Song.from_orm(i) for i in get_songs_from_db(db_session, song_ids=song_ids)]
