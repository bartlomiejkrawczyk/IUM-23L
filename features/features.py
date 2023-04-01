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
        t.release_date_s AS release_date_s,
        CAST(t.release_date_s AS timestamp) AS release_date,
        t.duration_ms AS duration_ms,

        t.explicit == 1 AS explicit,
        t.explicit AS explicit_numerical,
        
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

# I could add here avg, median, min, max, standard variation itp. itd.
artists_tracks = f"""--sql
    SELECT
        artist_id,
        genres,
        number_of_genres,
        COLLECT_LIST(track_id) AS artist_track_ids,
        COUNT(track_id) AS number_of_tracks,
        AVG(duration_ms) AS average_duration,

        CAST(MIN(release_date_s) AS timestamp) AS career_start,
        CAST(AVG(release_date_s) AS timestamp) AS average_release_date,
        CAST(MAX(release_date_s) AS timestamp) AS career_end,
        MAX(release_date_s) - MIN(release_date_s) AS career_duration_s,

        AVG(explicit_numerical) AS explicit_songs_ratio,
        AVG(popularity) AS average_popularity,
        AVG(acousticness) AS average_acousticness,
        AVG(danceability) AS average_danceability,
        AVG(energy) AS average_energy,
        AVG(instrumentalness) AS average_instrumentalness,
        AVG(liveness) AS average_liveness,
        AVG(loudness) AS average_loudness,
        AVG(speechiness) AS average_speechiness,
        AVG(tempo) AS average_tempo,
        AVG(valence) AS average_valence,

        AVG(track_name_length) AS average_track_name_length,

        AVG(daily_cost) AS average_daily_cost,

        COUNT_IF(storage_class == 'FAST') AS number_of_fast_storage_used,
        COUNT_IF(storage_class == 'FAST') AS number_of_fast_storage_used,
    FROM ({artists})
    INNER JOIN ({tracks}) USING (artist_id)
    GROUP BY artist_id, genres, number_of_genres
"""

track_genres = f"""--sql
    SELECT
        track_id,
        artist_id,
        genres
    FROM ({tracks})
    INNER JOIN ({artists}) USING (artist_id)
"""

premium_users = f"""--sql
    SELECT
        user_id,
        premium_user,

        timestamp AS premium_timestamp

    FROM ({users})
    INNER JOIN ({sessions}) USING (user_id)
    WHERE premium_user AND event_type == 'BUY_PREMIUM'
"""

users_before_premium = f"""--sql
    SELECT
        user_id,
        premium_user,

        IFNULL(MIN(timestamp), NOW()) AS non_premium_up_to

    FROM ({users})
    LEFT JOIN ({sessions}) USING (user_id)
    WHERE event_type == 'BUY_PREMIUM' OR event_type IS NULL
    GROUP BY user_id, premium_user
"""

non_premium_sessions = f"""--sql
    SELECT
        *
    FROM ({sessions})
    INNER JOIN ({users_before_premium}) USING (user_id)
    WHERE timestamp < non_premium_up_to
"""

premium_sessions = f"""--sql
    SELECT
        *
    FROM ({sessions})
    INNER JOIN ({users_before_premium}) USING (user_id)
    WHERE timestamp > non_premium_up_to
"""

user_liked_tracks = f"""--sql
    SELECT
        user_id, 
        track_id
    FROM ({users})
    INNER JOIN ({sessions}) USING (user_id)
    INNER JOIN ({tracks}) USING (track_id)
    WHERE event_type == 'LIKE'
    GROUP BY user_id, track_id
"""

result = user_liked_tracks

spark.sql(result).show()
