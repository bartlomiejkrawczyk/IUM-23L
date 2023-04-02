from spark import createSession
from matplotlib import pyplot as plt
from udfs import register_udfs

from itertools import product  # type: ignore


# =========== #
#    VIEWS    #
# =========== #


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


# TODO: add groupped sessions with group by user_id, session_id and track_id
user_session_track = f"""--sql
    SELECT
        user_id,
        session_id,
        track_id,
        
        MIN(timestamp) AS track_session_start,
        MAX(timestamp) AS track_session_last_event,

        TOTAL_TIME_LISTENED_MS(COLLECT_LIST(event_type), COLLECT_LIST(timestamp_s), )

    FROM ({sessions})
    INNER JOIN 
    GROUP BY user_id, session_id, track_id
"""

grouped_session_1 = f"""--sql
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

# TODO: include information about tracks and different artists
grouped_session = f"""--sql
    SELECT
        *, 
        EXTRACT(YEAR FROM session_start) AS year, 
        EXTRACT(MONTH FROM session_start) AS month
    FROM ({grouped_session_1})
"""

grouped_monthly_sessions = f"""--sql
    SELECT
        user_id,
        year,
        month,
    FROM ({grouped_session})
    GROUP BY user_id, year, month
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
        COUNT_IF(storage_class == 'MEDIUM') AS number_of_medium_storage_used,
        COUNT_IF(storage_class == 'SLOW') AS number_of_slow_storage_used
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


# TODO
monthly_sessions = f"""--sql
"""

monthly_user_tracks = f"""--sql
    SELECT
        user_id,
        track_id,
        year,
        month,
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
    FROM ({tracks})
    INNER JOIN ({track_genres}) USING (track_id, artist_id)
    INNER JOIN ({sessions}) USING (track_id)
    INNER JOIN ({users}) USING (user_id)
    GROUP BY user_id, track_id, year, month, genres, favourite_genres, duration_ms
"""

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
    FROM ({tracks})
    INNER JOIN ({track_genres}) USING (track_id, artist_id)
    INNER JOIN ({sessions}) USING (track_id)
    INNER JOIN ({users}) USING (user_id)
    GROUP BY user_id, track_id, genres, favourite_genres, duration_ms
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

non_premium_sessions_event_ratio = f"""--sql
    SELECT
        year,
        month,
        CONCAT(CAST(year AS string), '-', CAST(month AS string)) AS date,

        COUNT_IF(event_type == 'PLAY') AS play_number,
        COUNT_IF(event_type == 'SKIP') AS skip_number,
        COUNT_IF(event_type == 'LIKE') AS like_number,
        COUNT_IF(event_type == 'ADVERTISEMENT') AS advertisement_number
    FROM ({non_premium_sessions})
    GROUP BY year, month
    ORDER BY year, month
"""


premium_sessions_event_ratio = f"""--sql
    SELECT
        year,
        month,
        CONCAT(CAST(year AS string), '-', CAST(month AS string)) AS date,

        COUNT_IF(event_type == 'PLAY') AS play_number,
        COUNT_IF(event_type == 'SKIP') AS skip_number,
        COUNT_IF(event_type == 'LIKE') AS like_number,
        COUNT_IF(event_type == 'ADVERTISEMENT') AS advertisement_number
    FROM ({premium_sessions})
    GROUP BY year, month
    ORDER BY year, month
"""


def non_premium_vs_premium_plot():
    columns = ['play_number', 'skip_number',
               'like_number', 'advertisement_number']
    _, axs = plt.subplots(1, 2, figsize=(24, 6), sharey=True)

    spark.sql(non_premium_sessions_event_ratio) \
        .toPandas() \
        .plot \
        .bar(x='date', y=columns, ax=axs[0])  # type: ignore

    axs[0].set_title('non-premium')

    spark.sql(premium_sessions_event_ratio) \
        .toPandas() \
        .plot \
        .bar(x='date', y=columns, ax=axs[1])  # type: ignore

    axs[1].set_title('premium')

    plt.show()


positive_loudness_tracks = f"""--sql
    SELECT
        COUNT(*)
    FROM tracks
    WHERE loudness > 0
"""

# =================================== #
#    GROUP BY USER_ID, YEAR, MONTH    #
# =================================== #


# ================== #
#      FEATURES      #
# ================== #

# Postaraj się odpowiedzieć na pytanie - Czy dany użytkownik kupi w tym miesiącu premium?

interesting_months = f"""--sql
    SELECT * FROM months
"""

user_monthly_stats = f"""--sql
    SELECT
        *
    FROM ({users})
    GROUP BY user_id, year, month
"""

# this should on per month basis
user_history_up_to_buy_premium = f"""--sql
    SELECT
        *
    FROM ({user_monthly_stats})
    INNER JOIN ({users_before_premium}) USING (user_id)
    WHERE timestamp < non_premium_up_to
"""

# history up to given month
user_whole_history_stats = f"""--sql
    SELECT
        *
    FROM ({user_monthly_stats})
    GROUP BY user_id
"""

result = f"""--sql
    SELECT
        *
    FROM ({users})
    INNER JOIN 
    GROUP BY user_id, year, month
"""


if __name__ == '__main__':

    spark = createSession()

    month_columns = ['year', 'month']
    months = product(range(2019, 2024), range(1, 13))

    spark.createDataFrame(data=months, schema=month_columns) \
        .createOrReplaceTempView('months')

    register_udfs(spark)
    result = interesting_months
    spark.sql(result).show()
    # non_premium_vs_premium_plot()
