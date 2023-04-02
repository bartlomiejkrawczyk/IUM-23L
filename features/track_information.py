from spark import createSession

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


tracks_information = f"""--sql
    SELECT
        *
    FROM ({tracks})
    INNER JOIN ({artists}) USING (artist_id)
"""


if __name__ == '__main__':
    spark = createSession()
    result = tracks_information

    spark.sql(result).show()
