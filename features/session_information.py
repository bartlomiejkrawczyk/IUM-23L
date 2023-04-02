from spark import createSession
from track_information import track_information

session_information_1 = f"""--sql
    SELECT
        *
    FROM sessions
    LEFT JOIN ({track_information}) USING (track_id)
    LEFT JOIN user_tracks USING (user_id, track_id)
    INNER JOIN users USING (user_id)
"""

session_information = f"""--sql
    SELECT
        -- session specific
        user_id,
        session_id,
        premium_user,

        COLLECT_LIST(track_id) AS track_ids,
        COLLECT_LIST(event_type) AS event_types,

        COUNT_IF(event_type == 'BUY_PREMIUM') AS number_of_premium,

        COUNT_IF(event_type == 'ADVERTISEMENT') AS number_of_advertisements,
        COUNT_IF(event_type == 'PLAY') AS number_of_tracks,
        COUNT_IF(event_type == 'SKIP') AS number_of_skips,
        COUNT_IF(event_type == 'LIKE') AS number_of_likes,

        MIN(timestamp) AS session_start,
        MAX(timestamp) AS session_last_event,
        
        MAX(timestamp_s) - MIN(timestamp_s) AS session_duration,
        -- user tracks specific

        COUNT_IF(liked_track) AS number_of_liked_tracks,
        AVG(total_time_listened_ms) AS total_time_listened_to_a_track,

        -- tracks specific

        COLLECT_LIST(DISTINCT artist_id) AS different_artists,
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
    GROUP BY user_id, session_id, premium_user
"""


if __name__ == '__main__':
    spark = createSession()
    result = session_information

    spark.sql(result).show()
