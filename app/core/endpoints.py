from fastapi import APIRouter, Depends
from app.core.database_crud import create_listening_history_record
from app.core.dependencies import get_song_or_404
from app.users.dependencies import get_current_user
from app.database.dependency import get_db

router = APIRouter(
    prefix="/songs"
)

@router.post("/history/{song_id}")
def listen_to_song(
    song = Depends(get_song_or_404),
    database_conn = Depends(get_db),
    user = Depends(get_current_user)
):
    create_listening_history_record(database_conn, song.id, user.id)


@router.get("/history")
def get_listening_history(
    database_conn = Depends(get_db),
    user = Depends(get_current_user)
):
    pass

