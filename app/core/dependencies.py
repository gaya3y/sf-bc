from fastapi import Body, Depends, HTTPException
from app.core.database_crud import get_history_by_id, get_song_by_id
from app.database.dependency import get_db
from app.users.dependencies import get_current_user


def get_song_or_404(song_id: int = Body(...), database_conn = Depends(get_db)):
    song = get_song_by_id(database_conn, song_id)
    if song is None:
        raise HTTPException(status_code=404, detail="Song not found")
    return song


def get_history_or_404(history_id: int, database_conn = Depends(get_db), user = Depends(get_current_user)):
    history = get_history_by_id(database_conn, history_id)
    if history is None:
        raise HTTPException(status_code=404, detail="History not found")
    if history.user_id != user.id or history.end_time is not None:
        raise HTTPException(status_code=403, detail="Permission denied")

    return history
