from app.core.models import ListeningHistory, Song

def create_listening_history_record(connecion, song_id, user_id):
    record = ListeningHistory(song_id=song_id, user_id=user_id)
    connecion.add(record)
    connecion.commit()


def get_song_by_id(connection, song_id):
    return connection.query(Song).get(song_id)

