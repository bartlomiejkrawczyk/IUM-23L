from spark import createSession
from config import VIEWS

from pyspark.sql.dataframe import DataFrame
import pyspark.sql.functions as F
# import pyspark.sql.types as T

from typing import List

import shutil

spark = createSession()


def get_columns_of_type(data_frame: DataFrame, type: str) -> List[str]:
    return [column[0] for column in data_frame.dtypes if column[1] == type]


def register_tables() -> None:
    shutil.rmtree('./spark-warehouse/')

    for view, file in VIEWS.items():
        spark.sql(f'DROP TABLE IF EXISTS {view}').show()
        df = spark.read.json(file)
        # for column in get_columns_of_type(df, 'boolean'):
        #     df = df.withColumn(column, F.col(column).cast(T.IntegerType()))

        for column in df.columns:
            if column in ['timestamp', 'release_date']:
                df = df.withColumn(f'{column}_s', F.unix_timestamp(
                    column, "yyyy[-MM-dd['T'HH:mm:ss[.SSSSSS]]]"))
        df.write.mode('overwrite').saveAsTable(view, mode='overwrite')


if __name__ == '__main__':
    register_tables()
