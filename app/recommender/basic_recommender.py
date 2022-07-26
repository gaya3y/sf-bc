from datetime import timedelta
import logging
from app.core.database_crud import get_listening_history_of_user, get_songs_from_db
from app.core.datamodels import Song
from app.database.dependency import get_db
from app.recommender.db_crud import db_get_favorite_songs, db_get_popular_songs_by_genre
from app.users.database_crud import get_user_by_id, list_user
from app.users.datamodels import User


class BasicRecommender:

    GENRE_WEIGHT = 0.65
    ARTIST_WEIGHT = 0.35

    def compute_artists_genres_weights(db_session, user_id):
        user_favourites = db_get_favorite_songs(db_session, user_id)
        songs = get_songs_from_db(
            db_session,
            song_ids=[song["song_id"] for song in user_favourites]
        )

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
        return weighed_genres, weighed_artists


    @classmethod
    def recommend_songs(cls, db_session, user_id):
        weighed_genres, weighed_artists = cls.compute_artists_genres_weights(db_session, user_id)
        recommendations = []
        user_listened_recently = [
            record.song_id for record in
            get_listening_history_of_user(
                db_session,
                user_id,
                timedelta=timedelta(days=30)
            )
        ]
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
                "song": Song.from_orm(next(filter(lambda x: x.id == song_id, songs))),
                "weight": sum([song["weight"] for song in recommendations if song["song_id"] == song_id])
            })
        return sorted(final_recommendations, key=lambda x: x["weight"], reverse=True)

    @classmethod
    def recommend_users(cls, db_session, user_id, count=10):
        current_weighed_genres, current_weighed_artists = cls.compute_artists_genres_weights(db_session, user_id)
        current_offset = 0
        targets = []
        cutoff = 0.5
        current_user = get_user_by_id(db_session, user_id)
        following = [i.id for i in current_user.following]
        while len(targets) < count:
            users = list_user(db_session, 500, current_offset)
            if len(users) == 0:
                break
            for user in users:
                if user.id == user_id or user.id in following:
                    continue
                weighed_genres, weighed_artists = cls.compute_artists_genres_weights(db_session, user.id)
                all_genres = set(current_weighed_genres.keys()) | set(weighed_genres.keys())
                all_artists = set(current_weighed_artists.keys()) | set(weighed_artists.keys())
                genre_compability = max(1 - sum([abs(current_weighed_genres.get(genre, 0) - weighed_genres.get(genre, 0)) for genre in all_genres]), 0)
                artists_compabilty = max(1 - sum([abs(current_weighed_artists.get(artist, 0) - weighed_artists.get(artist, 0)) for artist in all_artists]), 0)
                compability_diff = genre_compability * cls.GENRE_WEIGHT + artists_compabilty * cls.ARTIST_WEIGHT
                if compability_diff > cutoff:
                    targets.append({
                        "user": User.from_orm(user),
                        "compability": compability_diff
                    })
            current_offset += 1
        return sorted(targets, key=lambda x: x["compability"], reverse=True)[:count]
