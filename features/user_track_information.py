from spark import createSession
from udfs import register_udfs
from track_information import track_information

user_liked_tracks = f"""--sql
    SELECT
        user_id,
        track_id,
        MIN(timestamp) AS date_liked
    FROM sessions
    WHERE event_type == 'LIKE'
    GROUP BY user_id, track_id
"""

user_tracks = f"""--sql
    SELECT
        user_id,
        track_id,
        date_liked IS NOT NULL AS liked,
        date_liked,
        SIZE(ARRAY_INTERSECT(genres, favourite_genres)) AS number_of_user_track_favourite_genres
    FROM ({track_information})
    INNER JOIN sessions USING (track_id)
    INNER JOIN users USING (user_id)
    LEFT JOIN ({user_liked_tracks}) USING (user_id, track_id)
    GROUP BY user_id, track_id, genres, favourite_genres, date_liked
"""


if __name__ == '__main__':
    spark = createSession()
    register_udfs(spark)
    result = user_tracks
    spark.sql(result) \
        .write \
        .mode(saveMode='overwrite') \
        .saveAsTable('user_tracks')
