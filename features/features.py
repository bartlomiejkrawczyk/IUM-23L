from spark import createSession

spark = createSession()

users = f"""--sql
    SELECT
        user_id,
        premium_user,
        favourite_genres,
        SIZE(favourite_genres) AS number_of_favourite_genres
    FROM users
"""

sessions_1 = f"""--sql
    SELECT
        user_id,
        session_id,
        track_id,
        event_type,
        timestamp_s,
        CAST(timestamp_s AS timestamp) AS timestamp
    FROM sessions
"""

sessions = f"""--sql
    SELECT
        *,
        EXTRACT(YEAR FROM timestamp) AS year,
        EXTRACT(MONTH FROM timestamp) AS month,
        EXTRACT(DAY FROM timestamp) AS day,
        EXTRACT(DAYOFWEEK FROM timestamp) AS day_of_week -- Sunday(1) to Saturday(7)
    FROM ({sessions_1})
"""

grouped_session = f"""--sql
    SELECT
        user_id,
        session_id,
        COLLECT_LIST(track_id) AS track_ids,
        COLLECT_LIST(event_type) AS event_types,

        COUNT_IF(event_type == 'BUY_PREMIUM') AS number_of_premium,

        COUNT_IF(event_type == 'ADVERTISEMENT') AS number_of_advertisements,
        COUNT_IF(event_type == 'PLAY') AS number_of_songs,
        COUNT_IF(event_type == 'SKIP') AS number_of_skips,
        COUNT_IF(event_type == 'LIKE') AS number_of_likes,

        MIN(timestamp) AS session_start,
        MAX(timestamp) AS session_last_event,
        
        CAST(MAX(timestamp) AS long) - CAST(MIN(timestamp) AS long) AS session_duration
    FROM ({sessions})
    GROUP BY user_id, session_id
    ORDER BY session_duration DESC
"""


artists = f"""--sql
    SELECT
        id AS artist_id,
        CHARACTER_LENGTH(name) AS artist_name_length,
        genres,
        SIZE(genres) AS number_of_genres
    FROM artists
"""

tracks_1 = f"""--sql
    SELECT
        t.id AS track_id,
        t.id_artist AS artist_id,
        t.popularity AS popularity,
        t.release_date_s AS release_date_s,
        CAST(t.release_date_s AS timestamp) AS release_date,
        t.duration_ms AS duration_ms,

        t.explicit == 1 AS explicit,
        
        t.key AS key,
        t.popularity AS popularity,

        t.acousticness AS acousticness,
        t.danceability AS danceability,
        t.energy AS energy,
        t.instrumentalness AS instrumentalness,
        t.liveness AS liveness,
        t.loudness AS loudness,
        t.speechiness AS speechiness,
        t.tempo AS tempo,
        t.valence AS valence,

        CHARACTER_LENGTH(t.name) AS track_name_length,

        ts.daily_cost AS daily_cost,
        ts.storage_class AS storage_class
    FROM tracks AS t
    INNER JOIN track_storage AS ts on t.id == ts.track_id
"""

tracks = f"""--sql
    SELECT
        *,
        EXTRACT(YEAR FROM release_date) AS release_year,
        EXTRACT(MONTH FROM release_date) AS release_month,
        EXTRACT(DAY FROM release_date) AS release_day
    FROM ({tracks_1})
"""

artists_tracks = f"""--sql

"""

result = grouped_session

spark.sql(result).show()
