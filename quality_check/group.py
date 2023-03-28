from spark import createSession
from config import VIEWS, DATE_FORMAT

spark = createSession()


def register_views() -> None:
    for view, file in VIEWS.items():
        df = spark.read.json(file)
        df.createOrReplaceTempView(view)


def session_info() -> str:
    info = f"""--sql
        SELECT
            session_id,
            user_id,
            MIN(timestamp) AS min, 
            MAX(timestamp) AS max,
            COLLECT_LIST(event_type),
            COLLECT_LIST(track_id)
        FROM sessions
        GROUP BY session_id, user_id
    """

    return f"""--sql
        SELECT
            *,
            UNIX_TIMESTAMP(max, "{DATE_FORMAT}") - UNIX_TIMESTAMP(min, "{DATE_FORMAT}") AS duration
        FROM ({info})
    """


def analyze() -> None:
    spark.sql(session_info()).show()


def main() -> None:
    register_views()
    analyze()


if __name__ == '__main__':
    main()
