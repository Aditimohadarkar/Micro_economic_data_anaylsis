from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_timestamp, explode, size

def transform_extracted_csv(in_path : str, out_path :str):
    spark = SparkSession.builder.appName('job_transform').getOrCreate()
    df = spark.read.option('header', True).csv(in_path)
    cleaned = (
        df.select(
            col("series_id"),
            col("date"),
            col("value"),
        )
        .dropna(subset=["series_id", "date", "value"])
    )

    cleaned.write.mode("overwrite").option("header", True).csv(out_path)
    spark.stop()