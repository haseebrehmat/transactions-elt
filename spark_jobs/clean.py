import sys
from common import get_spark_session, write_stage_snapshot, write_iceberg_table
from pyspark.sql.functions import col, trim, upper


def clean_transactions(execution_folder):
    spark = get_spark_session("T2 - Basic Cleansing")

    # Read from Iceberg Raw
    df_raw = spark.table("iceberg.bank.raw_transactions")

    # Drop rows with nulls in essential columns
    # txn_id, customer_id, txn_amount, txn_date
    df_cleaned = df_raw.dropna(
        subset=["txn_id", "customer_id", "txn_amount", "txn_date"]
    )

    # Standardize field formats
    df_cleaned = (
        df_cleaned.withColumn("txn_type", upper(trim(col("txn_type"))))
        .withColumn("currency", upper(trim(col("currency"))))
        .withColumn("status", upper(trim(col("status"))))
    )

    # Write snapshot to pipeline-runs/
    write_stage_snapshot(df_cleaned, execution_folder, "2_basic_cleansing")

    # Write to Iceberg Clean Table
    write_iceberg_table(df_cleaned, "clean_transactions", mode="overwrite")
    print("Cleaning Successful.")
    spark.stop()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: clean.py <execution_folder>")
        sys.exit(1)
    clean_transactions(sys.argv[1])
