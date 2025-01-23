from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lit

spark = SparkSession.builder.appName("CP Users ETL").getOrCreate()

pml_df = spark.read.parquet("/data/gr/pml/data")

passport_df = (
    spark.read.format("jdbc")
    .option("url", "jdbc:postgresql://...")
    .option("dbtable", "public.passport_info")
    .option("user", "user")
    .option("password", "password")
    .load()
    .select(col("user_id"), col("sex").alias("doc_sex"), col("age").alias("doc_age"))
)

joined_df = pml_df.join(passport_df, on="user_id", how="left")

final_df = joined_df.select(col("user_id"), col("predicted_sex"), col("predicted_age"), col("doc_sex"), col("doc_age"))

final_df.write.mode("overwrite").parquet("/data/gr/cp/users")
