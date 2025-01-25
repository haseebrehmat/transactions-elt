from pyspark.sql import SparkSession
import os


def get_spark_session(app_name):
    # Configuration for Iceberg + MinIO (S3 Compatible)
    aws_access_key = os.getenv("AWS_ACCESS_KEY_ID", "admin")
    aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY", "password123")
    minio_endpoint = os.getenv("MINIO_ENDPOINT", "http://minio:9000")

    spark = (
        SparkSession.builder.appName(app_name)
        # Iceberg Spark SQL Extensions
        .config(
            "spark.sql.extensions",
            "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions",
        )
        # Iceberg Catalog Configuration (Hadoop Catalog on S3)
        .config("spark.sql.catalog.iceberg", "org.apache.iceberg.spark.SparkCatalog")
        .config("spark.sql.catalog.iceberg.type", "hadoop")
        .config("spark.sql.catalog.iceberg.warehouse", "s3a://iceberg-warehouse/")
        # S3 / MinIO Configuration
        .config("spark.hadoop.fs.s3a.endpoint", minio_endpoint)
        .config("spark.hadoop.fs.s3a.access.key", aws_access_key)
        .config("spark.hadoop.fs.s3a.secret.key", aws_secret_key)
        .config("spark.hadoop.fs.s3a.path.style.access", "true")
        .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
        .config("spark.hadoop.fs.s3a.connection.ssl.enabled", "false")
        # Global Warehouse Fix
        .config("spark.sql.warehouse.dir", "s3a://iceberg-warehouse/")
        # Optimization
        .config("spark.sql.catalog.iceberg.cache-enabled", "false")
        .getOrCreate()
    )

    # Ensure the database/namespace exists in Iceberg
    spark.sql("CREATE NAMESPACE IF NOT EXISTS iceberg.bank")

    return spark


def write_stage_snapshot(df, execution_folder, stage_name):
    """Writes a dataframe snapshot as CSV to the execution folder in MinIO."""
    output_path = f"s3a://pipeline-runs/{execution_folder}/{stage_name}"
    print(f"Saving snapshot to: {output_path}")
    df.coalesce(1).write.mode("overwrite").option("header", "true").csv(output_path)


def write_iceberg_table(df, table_name, mode="append"):
    """Writes a dataframe to an Iceberg table in the iceberg.bank namespace."""
    full_table_name = f"iceberg.bank.{table_name}"
    print(f"Writing to Iceberg table: {full_table_name} with mode: {mode}")

    spark = df.sparkSession
    if mode == "overwrite":
        df.writeTo(full_table_name).createOrReplace()
    else:
        if spark.catalog.tableExists(full_table_name):
            df.writeTo(full_table_name).append()
        else:
            df.writeTo(full_table_name).create()
