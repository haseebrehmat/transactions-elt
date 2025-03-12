import sys
from common import get_spark_session, write_stage_snapshot, write_iceberg_table
from pyspark.sql.functions import col, to_date, when


def enrich_transactions(execution_folder):
    spark = get_spark_session("T5 - Feature Enrichment")

    # Read from Iceberg Success
    df_success = spark.table("iceberg.bank.success_transactions")

    # Add derived fields
    # txn_day (Date)
    # is_high_value (txn_amount > 10000)
    df_enriched = df_success.withColumn("txn_day", to_date(col("txn_ts"))).withColumn(
        "is_high_value", when(col("txn_amount") > 10000, True).otherwise(False)
    )

    # Write snapshot to pipeline-runs/
    write_stage_snapshot(df_enriched, execution_folder, "5_feature_enrichment")

    # Write to Iceberg Enriched Table
    write_iceberg_table(df_enriched, "enriched_transactions", mode="overwrite")
    print("Enrichment Successful.")
    spark.stop()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: enrich.py <execution_folder>")
        sys.exit(1)
    enrich_transactions(sys.argv[1])
