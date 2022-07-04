from fastapi import Depends, HTTPException
from app.core.database_crud import get_song_by_id
from app.database.dependency import get_db


def get_song_or_404(song_id: int, database_conn = Depends(get_db)):
    song = get_song_by_id(database_conn, song_id)
    if song is None:
        raise HTTPException(status_code=404, detail="Song not found")
    return song
