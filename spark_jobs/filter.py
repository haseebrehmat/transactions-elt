import sys
from common import get_spark_session, write_stage_snapshot, write_iceberg_table
from pyspark.sql.functions import col


def filter_success(execution_folder):
    spark = get_spark_session("T4 - Filter Out Failed")

    # Read from Iceberg Normalized
    df_normalized = spark.table("iceberg.bank.normalized_transactions")

    # Filter: status != 'FAILED'
    df_successful = df_normalized.filter(col("status") != "FAILED")

    # Write snapshot to pipeline-runs/
    write_stage_snapshot(df_successful, execution_folder, "4_filter_success")

    # Write to Iceberg Success Table
    write_iceberg_table(df_successful, "success_transactions", mode="overwrite")
    print("Filtering Successful.")
    spark.stop()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: filter.py <execution_folder>")
        sys.exit(1)
    filter_success(sys.argv[1])
