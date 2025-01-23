from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, withColumn

spark = SparkSession.builder.appName("PML Data ETL").getOrCreate()

pml_raw_df = spark.read.format("parquet").load("/data/pml/predictions_raw")

final_df = pml_raw_df.select(
    col("user_id"),
    withColumn("predicted_sex", when(col("predicted_sex") == 1, "M").when(col("predicted_sex") == 0, "F")),
    col("predicted_age").alias("age_model"),
)

final_df.write.mode("overwrite").parquet("/data/gr/pml/data")
