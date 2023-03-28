# Import SparkSession
from pyspark.sql import SparkSession

# Create SparkSession
spark = SparkSession.builder \
    .master("local[1]") \
    .appName("SparkByExamples.com") \
    .getOrCreate()

VIEWS = {
    'artists': "../data/v1/artists.jsonl",
    'sessions': "../data/v1/sessions.jsonl",
    'track_storage': "../data/v1/track_storage.jsonl",
    'tracks': "../data/v1/tracks.jsonl",
    'users': "../data/v1/users.jsonl",
}

NUMBER_COLUMNS = {
    'artists': [],
    'sessions': ['session_id',  'user_id'],  # timestamp
    'track_storage': ['daily_cost'],
    'tracks': ['acousticness', 'danceability', 'duration_ms', 'energy', 'explicit', 'instrumentalness', 'key', 'liveness', 'loudness', 'popularity', 'speechiness', 'tempo', 'valence'],
    'users': ['user_id'],
}


LIST_COLUMNS = {
    'artists': ['genres'],
    'sessions': [],
    'track_storage': [],
    'tracks': [],
    'users': ['favourite_genres'],
}

for view, file in VIEWS.items():
    df = spark.read.json(file)
    df.createOrReplaceTempView(view)

print('Users')


for view in VIEWS.keys():
    print("=" * 120)
    print(view)
    dataframe = spark.sql(f"""--sql
        SELECT 
            * 
        FROM {view}
    """)

    dataframe.show()

    spark.sql(f"""--sql
        SELECT 
            COUNT(*) AS length
        FROM {view}
    """).show()

    for column in dataframe.columns:
        print(column)

        spark.sql(f"""--sql
            SELECT 
                {column},
                COUNT(*) AS length
            FROM {view}
            GROUP BY {column}
            ORDER BY {column} NULLS FIRST
        """).show()

        spark.sql(f"""--sql
            SELECT
                COUNT(DISTINCT {column})
            FROM {view}
        """).show()

    for column in NUMBER_COLUMNS[view]:
        print(column)

        spark.sql(f"""--sql
            SELECT 
                COUNT({column}) AS count,
                MIN({column}) AS min,
                MAX({column}) AS max,
                AVG({column}) AS average,
                SUM({column}) AS sum,
                SUM(DISTINCT {column}) AS sum,
                KURTOSIS({column}) AS kurtosis,
                SKEWNESS({column}) AS skewness,
                STDDEV({column}) AS standard_deviation,
                STDDEV_POP({column}) AS population_standard_deviation,
                VARIANCE({column}) AS variance,
                VAR_POP({column}) AS population_variance
            FROM {view}
            WHERE {column} IS NOT NULL
        """).show()

    for column in LIST_COLUMNS[view]:
        print(column)

        spark.sql(f"""--sql
            SELECT
                DISTINCT EXPLODE({column}) AS {column}
            FROM {view}
            ORDER BY {column} NULLS FIRST
        """).show()

        spark.sql(f"""--sql
            SELECT
                COUNT(*) AS length
            FROM (
                SELECT
                    DISTINCT EXPLODE({column}) AS {column}
                FROM {view}
            )
        """).show()
