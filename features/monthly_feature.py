from spark import createSession
from track_information import track_information
from non_premium_vs_premium import bought_premium

sessions_with_tracks = f"""--sql
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
    FROM ({sessions_with_tracks})
    LEFT JOIN ({track_information}) USING (track_id)
    LEFT JOIN user_tracks USING (user_id, track_id)
    INNER JOIN users USING (user_id)
    LEFT JOIN ({bought_premium}) USING (user_id, premium_user)
"""

monthly_session_information = f"""--sql
    SELECT
        -- session specific
        user_id,
        EXTRACT(YEAR FROM MIN(timestamp)) AS year,
        EXTRACT(MONTH FROM MIN(timestamp)) AS month,

        -- premium_user,
        premium_user_numerical,

        -- MONTHS_BETWEEN(non_premium_up_to, MIN(timestamp)) AS months_till_premium,
        -- MONTHS_BETWEEN(non_premium_up_to, MIN(timestamp)) <= 1 AS will_buy_premium_next_month,
        CAST(IFNULL(MONTHS_BETWEEN(non_premium_up_to, MIN(timestamp)) <= 1, FALSE) AS INTEGER) AS will_buy_premium_next_month_numerical,
        -- non_premium_up_to,
        -- ANY(IFNULL(timestamp > non_premium_up_to, False)) AS had_premium,
        -- CAST(ANY(IFNULL(timestamp > non_premium_up_to, False)) AS INTEGER) AS had_premium_numerical,

        -- COLLECT_LIST(track_id) AS track_ids,
        -- COLLECT_LIST(event_type) AS event_types,

        COUNT_IF(event_type == 'BUY_PREMIUM') AS number_of_premium,

        COUNT_IF(event_type == 'ADVERTISEMENT') AS number_of_advertisements,
        COUNT_IF(event_type == 'PLAY') AS number_of_tracks,
        COUNT_IF(event_type == 'SKIP') AS number_of_skips,
        COUNT_IF(event_type == 'LIKE') AS number_of_likes,


        -- MIN(timestamp) AS session_start,
        -- MAX(timestamp) AS session_last_event,
        
        -- MAX(timestamp_s) - MIN(timestamp_s) AS session_duration,
        -- user tracks specific

        COUNT_IF(IFNULL(timestamp <= date_liked, FALSE)) AS number_of_liked_tracks_listened,
        COUNT_IF(IFNULL(number_of_user_track_favourite_genres > 0, FALSE)) AS number_of_tracks_in_favourite_genre,
        IFNULL(SUM(number_of_user_track_favourite_genres), 0) AS total_number_of_favourite_genres_listened,

        IFNULL(AVG(CASE WHEN number_of_user_track_favourite_genres > 0 THEN popularity ELSE NULL END), 0) AS average_popularity_in_favourite_genres,
        
        -- tracks specific
        IFNULL(SUM(duration_ms), 0) AS total_tracks_duration_ms,

        COUNT(DISTINCT artist_id) AS number_of_different_artists,

        IFNULL(AVG(release_date_s), 0) AS average_release_date,
        IFNULL(AVG(duration_ms), 0) AS average_duration_ms,

        IFNULL(AVG(explicit_numerical), 0) AS explicit_tracks_ratio,
        
        IFNULL(AVG(popularity), 0) AS average_popularity,
        IFNULL(AVG(acousticness), 0) AS average_acousticness,
        IFNULL(AVG(danceability), 0) AS average_danceability,
        IFNULL(AVG(energy), 0) AS average_energy,
        IFNULL(AVG(instrumentalness), 0) AS average_instrumentalness,
        IFNULL(AVG(liveness), 0) AS average_liveness,
        IFNULL(AVG(loudness), 0) AS average_loudness,
        IFNULL(AVG(speechiness), 0) AS average_speechiness,
        IFNULL(AVG(tempo), 0) AS average_tempo,
        IFNULL(AVG(valence), 0) AS average_valence,

        IFNULL(AVG(track_name_length), 0) AS average_track_name_length,

        IFNULL(AVG(daily_cost), 0) AS average_daily_cost
    FROM ({session_information_1})
    GROUP BY user_id, session_id, EXTRACT(YEAR FROM timestamp), EXTRACT(MONTH FROM timestamp), premium_user, premium_user_numerical, non_premium_up_to
    HAVING NOT ANY(IFNULL(timestamp > non_premium_up_to, False))
"""

if __name__ == '__main__':
    spark = createSession()

    result = monthly_session_information
    spark.sql(result).coalesce(1).write.csv('feature.csv', header=True)
