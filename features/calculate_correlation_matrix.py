from pyspark.ml.stat import Correlation
from pyspark.ml.feature import VectorAssembler
from spark import createSession
# from pyspark.sql.functions import lit
from session_information import session_information
spark = createSession()

df = spark.sql(f'SELECT * FROM ({session_information})')
# df = df.withColumn('target', F.lit('1').cast('bigint'))

method = 'pearson'
# method = 'spearman'

columns = []

for column, type in df.dtypes:
    if type in ['int', 'boolean', 'double', 'bigint'] and not '_id' in column:
        columns.append(column)

# convert to vector column first
vector_col = "corr_features"
assembler = VectorAssembler(inputCols=columns, outputCol=vector_col)
df_vector = assembler.transform(df).select(vector_col)

# get correlation matrix
matrix = Correlation.corr(df_vector, vector_col, method=method)

values = matrix.collect()[0][f"{method}({vector_col})"].values

print(f"{' ': <30}", end='\t|\t')
for column in columns:
    print(f"{column: <30}", end='\t|\t')
print()
print('-|-' * (len(columns)))

for y, column in enumerate(columns):
    print(f"{columns[y]: <30}", end='\t|\t')
    for x in range(len(columns)):
        print(f"{values[y * len(columns) + x]: <30}", end='\t|\t')
    print()