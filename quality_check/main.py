from spark import createSession
from config import VIEWS, NUMBER_COLUMNS, LIST_COLUMNS

spark = createSession()


def register_views() -> None:
    for view, file in VIEWS.items():
        df = spark.read.json(file)
        df.createOrReplaceTempView(view)


def analyze() -> None:
    for view in VIEWS.keys():
        print("=" * 120)
        print(view)
        analyze_view(view)


def select_everything_from(view: str) -> str:
    return f"""--sql
        SELECT 
            * 
        FROM {view}
    """


def select_count_everything_from(view: str) -> str:
    return f"""--sql
        SELECT 
            COUNT(*) AS length
        FROM {view}
    """


def analyze_view(view: str) -> None:
    dataframe = spark.sql(select_everything_from(view))
    dataframe.show()
    spark.sql(select_count_everything_from(view)).show()

    for column in dataframe.columns:
        analyze_column(view, column)


def group_by_column(view: str, column: str) -> str:
    return f"""--sql
        SELECT 
            {column},
            COUNT(*) AS length
        FROM {view}
        GROUP BY {column}
        ORDER BY {column} IS NULL, length DESC, {column} NULLS FIRST
    """


def count_distinct_values(view: str, column: str) -> str:
    return f"""--sql
        SELECT
            COUNT(DISTINCT {column})
        FROM {view}
    """


def aggregate_numeric_column(view: str, column: str) -> str:
    return f"""--sql
            SELECT 
                COUNT({column}) AS count,
                MIN({column}) AS min,
                MAX({column}) AS max,
                AVG({column}) AS average,
                SUM({column}) AS sum,
                SUM(DISTINCT {column}) AS sumDistinct,
                KURTOSIS({column}) AS kurtosis,
                SKEWNESS({column}) AS skewness,
                STDDEV({column}) AS standard_deviation,
                STDDEV_POP({column}) AS population_standard_deviation,
                VARIANCE({column}) AS variance,
                VAR_POP({column}) AS population_variance
            FROM {view}
            WHERE {column} IS NOT NULL
        """


def explode_column(view: str, column: str) -> str:
    return f"""--sql
            SELECT
                DISTINCT EXPLODE({column}) AS {column}
            FROM {view}
            ORDER BY {column} NULLS FIRST
        """


def count_exploded_column(view: str, column: str) -> str:
    exploded = f"""--sql
        SELECT
            DISTINCT EXPLODE({column}) AS {column}
        FROM {view}
    """

    return f"""--sql
            SELECT
                COUNT(*) AS length
            FROM ({exploded})
        """


def analyze_column(view: str, column: str) -> None:
    print(column)
    spark.sql(group_by_column(view, column)).show()
    spark.sql(count_distinct_values(view, column)).show()

    if column in NUMBER_COLUMNS[view]:
        spark.sql(aggregate_numeric_column(view, column)).show()

    if column in LIST_COLUMNS[view]:
        spark.sql(explode_column(view, column)).show()
        spark.sql(count_exploded_column(view, column)).show()


def main() -> None:
    register_views()
    analyze()


if __name__ == '__main__':
    main()
