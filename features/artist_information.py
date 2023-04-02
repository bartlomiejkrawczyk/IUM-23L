from spark import createSession
from track_information import track_information

# I could add here avg, median, min, max, standard variation itp. itd.
artist_information = f"""--sql
    SELECT
        artist_id, 
        artist_name_length, 
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
    FROM ({track_information})
    GROUP BY artist_id, artist_name_length, genres, number_of_genres
"""

if __name__ == '__main__':
    spark = createSession()
    result = artist_information

    spark.sql(result).show()
