from spark import createSession
from udfs import register_udfs
from track_information import track_information

user_tracks = f"""--sql
    SELECT
        user_id,
        track_id,

        COUNT_IF(event_type == 'LIKE') AS number_of_likes,
        IFNULL(ANY(event_type == 'LIKE'), FALSE) AS liked_track,

        COUNT_IF(event_type == 'SKIP') AS number_of_skips,
        IFNULL(ANY(event_type == 'SKIP'), FALSE) AS skiped_track,

        COUNT_IF(event_type == 'PLAY') AS number_of_plays,
        IFNULL(ANY(event_type == 'PLAY'), FALSE) AS played_track,

        TOTAL_TIME_LISTENED_MS(COLLECT_LIST(event_type), COLLECT_LIST(timestamp_s), duration_ms) AS total_time_listened_ms,

        genres,
        favourite_genres,
        ARRAY_INTERSECT(genres, favourite_genres) AS user_track_favourite_genre
    FROM ({track_information})
    INNER JOIN sessions USING (track_id)
    INNER JOIN users USING (user_id)
    GROUP BY user_id, track_id, genres, favourite_genres, duration_ms
"""


if __name__ == '__main__':
    spark = createSession()
    register_udfs(spark)
    result = user_tracks
    spark.sql(result).show()
