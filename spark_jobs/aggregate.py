import sys
from common import get_spark_session, write_stage_snapshot, write_iceberg_table
from pyspark.sql.functions import col, count, sum, count_if


def aggregate_daily(execution_folder):
    spark = get_spark_session("T6 - Aggregations")

    # Read from Iceberg Enriched
    df_enriched = spark.table("iceberg.bank.enriched_transactions")

    # Group by txn_day and customer_id
    # Metrics:
    # Total transactions
    # Total amount
    # Count by txn_type (we'll do a simple high_value_count as per PRD)
    df_daily_summary = df_enriched.groupBy("txn_day", "customer_id").agg(
        count("txn_id").alias("total_txns"),
        sum("txn_amount").alias("total_amount"),
        count_if(col("is_high_value")).alias("high_value_count"),
    )

    # Write snapshot to pipeline-runs/
    write_stage_snapshot(df_daily_summary, execution_folder, "6_daily_aggregation")

    # Write to Final Iceberg Summary Table
    write_iceberg_table(df_daily_summary, "daily_transaction_summary", mode="overwrite")
    print("Aggregation Successful.")
    spark.stop()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: aggregate.py <execution_folder>")
        sys.exit(1)
    aggregate_daily(sys.argv[1])
