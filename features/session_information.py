from spark import createSession
from track_information import track_information
from non_premium_vs_premium import users_before_premium

sessions_with_tracks_ = f"""--sql
    SELECT
        session_id,
        timestamp,
        timestamp_s,
        CASE WHEN event_type == 'PLAY' THEN track_id ELSE NULL END AS track_id,
        user_id,
        event_type
    FROM sessions
"""

session_information_1 = f"""--sql
    SELECT
        *
    FROM ({sessions_with_tracks_})
    LEFT JOIN ({track_information}) USING (track_id)
    LEFT JOIN user_tracks USING (user_id, track_id)
    INNER JOIN users USING (user_id)
    INNER JOIN ({users_before_premium}) USING (user_id, premium_user)
"""

session_information = f"""--sql
    SELECT
        -- session specific
        user_id,
        session_id,
        premium_user,
        premium_user_numerical,

        ANY(timestamp > non_premium_up_to) AS had_premium,

        -- COLLECT_LIST(track_id) AS track_ids,
        -- COLLECT_LIST(event_type) AS event_types,

        COUNT_IF(event_type == 'BUY_PREMIUM') AS number_of_premium,

        COUNT_IF(event_type == 'ADVERTISEMENT') AS number_of_advertisements,
        COUNT_IF(event_type == 'PLAY') AS number_of_tracks,
        COUNT_IF(event_type == 'SKIP') AS number_of_skips, -- TODO: ignore skips
        COUNT_IF(event_type == 'LIKE') AS number_of_likes,

        EXTRACT(YEAR FROM MIN(timestamp)) AS year,
        EXTRACT(MONTH FROM MIN(timestamp)) AS month,

        -- MIN(timestamp) AS session_start,
        -- MAX(timestamp) AS session_last_event,
        
        MAX(timestamp_s) - MIN(timestamp_s) AS session_duration,
        -- user tracks specific

        COUNT_IF(IFNULL(timestamp <= date_liked, FALSE)) AS number_of_liked_tracks_listened,
        COUNT_IF(IFNULL(number_of_user_track_favourite_genres > 0, FALSE)) AS number_of_tracks_in_favourite_genre,
        SUM(number_of_user_track_favourite_genres) AS total_number_of_favourite_genres_listened,

        IFNULL(AVG(CASE WHEN number_of_user_track_favourite_genres > 0 THEN popularity ELSE NULL END), 0) AS average_popularity_in_favourite_genres,
        
        -- tracks specific
        SUM(duration_ms) AS total_tracks_duration_ms,

        COUNT(DISTINCT artist_id) AS number_of_different_artists,

        AVG(release_date_s) AS average_release_date,
        AVG(duration_ms) AS average_duration_ms,

        AVG(explicit_numerical) AS explicit_tracks_ratio,
        
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

        AVG(daily_cost) AS average_daily_cost
    FROM ({session_information_1})
    GROUP BY user_id, session_id, premium_user, premium_user_numerical
"""


if __name__ == '__main__':
    spark = createSession()
    result = session_information

    spark.sql(result).show()
