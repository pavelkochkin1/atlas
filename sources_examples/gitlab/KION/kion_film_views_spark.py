from pyspark.sql import SparkSession
from pyspark.sql.functions import col, countDistinct
from pyspark.sql.functions import sum as _sum

spark = SparkSession.builder.appName("KION Film Views ETL").getOrCreate()

film_views_df = spark.read.format("parquet").load("/data/kion/film_views_raw")
films_df = spark.read.format("parquet").load("/data/kion/films_info")

joined_df = film_views_df.join(films_df, film_views_df.film_id == films_df.film_id, how="left").select(
    film_views_df.user_id,
    film_views_df.film_id,
    col("films_df.title").alias("film_title"),
    film_views_df.watch_date,
    film_views_df.watch_duration,
    film_views_df.device_type,
)

agg_by_user = joined_df.groupBy("user_id").agg(
    _sum("watch_duration").alias("total_watch_duration"), countDistinct("film_id").alias("distinct_films_count")
)

final_df = joined_df.join(agg_by_user, on="user_id", how="left")

final_df.write.mode("overwrite").parquet("/data/kion/film_views")
