from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lit

spark = SparkSession.builder.appName("KION Users ETL").getOrCreate()

users_df = spark.read.format("csv").option("header", "true").load("/data/kion/users_raw")

clean_df = users_df.select(col("user_id"), col("sex"), col("age")).withColumn("source_system", lit("KION"))

clean_df.write.mode("overwrite").parquet("/data/kion/users")
