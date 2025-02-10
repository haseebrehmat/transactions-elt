from pyspark.sql.functions import current_date
import sys
from common import get_spark_session, write_stage_snapshot, write_iceberg_table


def ingest_raw(input_path, execution_folder):
    spark = get_spark_session("T1 - Raw Ingestion")

    # Read CSV from Raw S3 Bucket
    df_raw = (
        spark.read.option("header", "true")
        .option("inferSchema", "true")
        .csv(input_path)
    )

    # Write snapshot to pipeline-runs/
    write_stage_snapshot(df_raw, execution_folder, "1_raw_ingestion")

    df_raw = df_raw.withColumn("ingestion_date", current_date())

    # Use helper with overwrite mode since we read all CSVs from the bucket
    write_iceberg_table(df_raw, "raw_transactions", mode="overwrite")
    print("Ingestion Successful.")
    spark.stop()


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: ingest.py <input_path> <execution_folder>")
        sys.exit(1)
    ingest_raw(sys.argv[1], sys.argv[2])
