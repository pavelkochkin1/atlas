from pyspark.sql import SparkSession
from pyspark.sql.functions import col

spark = SparkSession.builder.appName("Stroki Users ETL").getOrCreate()

users_raw_df = spark.read.json("/data/stroki/users_raw")

clean_df = users_raw_df.select(col("user_id"), col("sex"), col("age"))

clean_df.write.mode("overwrite").parquet("/data/stroki/users")
