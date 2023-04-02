from spark import createSession
from matplotlib import pyplot as plt

users_before_premium = f"""--sql
    SELECT
        user_id,
        premium_user,

        IFNULL(MIN(timestamp), NOW()) AS non_premium_up_to

    FROM users
    LEFT JOIN sessions USING (user_id)
    WHERE event_type == 'BUY_PREMIUM' OR event_type IS NULL
    GROUP BY user_id, premium_user
"""

non_premium_sessions = f"""--sql
    SELECT
        *,
        EXTRACT(YEAR FROM timestamp) AS year,
        EXTRACT(MONTH FROM timestamp) AS month
    FROM sessions
    INNER JOIN ({users_before_premium}) USING (user_id)
    WHERE timestamp < non_premium_up_to
"""

premium_sessions = f"""--sql
    SELECT
        *,
        EXTRACT(YEAR FROM timestamp) AS year,
        EXTRACT(MONTH FROM timestamp) AS month
    FROM sessions
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


if __name__ == '__main__':

    spark = createSession()

    non_premium_vs_premium_plot()
