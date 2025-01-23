from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count
from pyspark.sql.functions import sum as _sum

spark = SparkSession.builder.appName("Stroki Readings ETL").getOrCreate()

reading_df = spark.read.json("/data/stroki/readings_raw")

reading_df = reading_df.withColumn("reading_duration", col("end_time").cast("long") - col("start_time").cast("long"))

agg_df = reading_df.groupBy("user_id").agg(
    _sum("reading_duration").alias("total_reading_duration"), count("book_id").alias("books_opened_count")
)

final_df = reading_df.join(agg_df, on="user_id", how="left")

final_df.write.mode("overwrite").parquet("/data/stroki/readings")
