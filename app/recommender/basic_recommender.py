from datetime import timedelta
from app.core.database_crud import get_listening_history_of_user, get_songs_from_db
from app.database.dependency import get_db
from app.recommender.db_crud import db_get_favorite_songs, db_get_popular_songs_by_genre


class BasicRecommender:

    GENRE_WEIGHT = 0.65
    ARTIST_WEIGHT = 0.35

    @classmethod
    def recommend_songs(cls, user_id):
        db_session = next(get_db())
        user_favourites = db_get_favorite_songs(db_session, user_id)
        songs = get_songs_from_db(
            db_session,
            song_ids=[song["song_id"] for song in user_favourites]
        )
        user_listened_recently = [
            record.song_id for record in
            get_listening_history_of_user(
                db_session,
                user_id,
                timedelta=timedelta(days=30)
            )
        ]

        genres = {}
        artists = {}
        for song in songs:
            for genre in song.genres:
                try:
                    genres[genre.id] += next(filter(lambda x: x["song_id"] == song.id, user_favourites))["duration"]
                except KeyError:
                    genres[genre.id] = next(filter(lambda x: x["song_id"] == song.id, user_favourites))["duration"]
            for artist in song.artists:
                try:
                    artists[artist.id] += next(filter(lambda x: x["song_id"] == song.id, user_favourites))["duration"]
                except KeyError:
                    artists[artist.id] = next(filter(lambda x: x["song_id"] == song.id, user_favourites))["duration"]

        total_duration = sum([song["duration"] for song in user_favourites], timedelta())
        weighed_genres = {
            genre_id: genres[genre_id] * BasicRecommender.GENRE_WEIGHT / total_duration
            for genre_id in genres 
        }
        weighed_artists = {
            artist_id: artists[artist_id] * BasicRecommender.ARTIST_WEIGHT / total_duration
            for artist_id in artists
        }
        recommendations = []

        for genre, weight in weighed_genres.items():
            count = weight // 0.1
            songs = db_get_popular_songs_by_genre(db_session, genre, user_listened_recently, count)
            i = 0
            if count == 0:
                continue
            for song in songs:
                song["weight"] = weight * (1 - i / count)
                i += 1
            recommendations.extend(songs)
        
        for genre, weight in weighed_artists.items():
            count = weight // 0.1
            if count == 0:
                continue
            i = 0
            for song in songs:
                song["weight"] = weight * (1 - i / count)
                i += 1
            recommendations.extend(songs)
        
        unique_recommendation_ids = set([song["song_id"] for song in recommendations])
        final_recommendations = []
        songs = get_songs_from_db(db_session, song_ids=unique_recommendation_ids)
        for song_id in unique_recommendation_ids:
            final_recommendations.append({
                "song": next(filter(lambda x: x.id == song_id, songs)),
                "weight": sum([song["weight"] for song in recommendations if song["song_id"] == song_id])
            })
        return sorted(final_recommendations, key=lambda x: x["weight"], reverse=True)
