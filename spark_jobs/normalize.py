import sys
from common import get_spark_session, write_stage_snapshot, write_iceberg_table
from pyspark.sql.functions import col, to_timestamp


def normalize_transactions(execution_folder):
    spark = get_spark_session("T3 - Parsing & Normalization")

    # Read from Iceberg Clean
    df_clean = spark.table("iceberg.bank.clean_transactions")

    # Convert types
    # txn_amount -> Decimal
    # txn_date -> Timestamp
    df_normalized = (
        df_clean.withColumn("txn_amount", col("txn_amount").cast("decimal(18,2)"))
        .withColumn("txn_ts", to_timestamp(col("txn_date")))
        .withColumn("txn_type_norm", col("txn_type"))
    )  # already upper in clean

    # Drop old txn_date and txn_type to avoid confusion
    df_normalized = df_normalized.drop("txn_date", "txn_type")

    # Write snapshot to pipeline-runs/
    write_stage_snapshot(df_normalized, execution_folder, "3_parsing_normalization")

    # Write to Iceberg Normalized Table
    write_iceberg_table(df_normalized, "normalized_transactions", mode="overwrite")
    print("Normalization Successful.")
    spark.stop()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: normalize.py <execution_folder>")
        sys.exit(1)
    normalize_transactions(sys.argv[1])
