from spark import createSession
from config import VIEWS

spark = createSession()


def register_views() -> None:
    for view, file in VIEWS.items():
        df = spark.read.json(file)
        df.createOrReplaceTempView(view)


def user_session_join() -> str:
    return f"""--sql
        SELECT
            *
        FROM sessions
        INNER JOIN users USING(user_id)
        WHERE event_type == "ADVERTISEMENT"
    """


def analyze() -> None:
    spark.sql(user_session_join()).show()


def main() -> None:
    register_views()
    analyze()


if __name__ == '__main__':
    main()
