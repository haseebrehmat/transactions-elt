from airflow import DAG
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
import os

default_args = {
    "owner": "antigravity",
    "depends_on_past": False,
    "start_date": datetime(2023, 1, 1),
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

# Paths to JARs in the Airflow container
JAR_PATH = "/opt/airflow/jars"
ICEBERG_JAR = f"{JAR_PATH}/iceberg-spark-runtime-3.5_2.12-1.4.2.jar"
AWS_BUNDLE_JAR = f"{JAR_PATH}/aws-java-sdk-bundle-1.12.262.jar"
HADOOP_AWS_JAR = f"{JAR_PATH}/hadoop-aws-3.3.4.jar"
ALL_JARS = f"{ICEBERG_JAR},{AWS_BUNDLE_JAR},{HADOOP_AWS_JAR}"

dag = DAG(
    "transaction_etl_dag",
    default_args=default_args,
    description="A distributed ETL pipeline for banking transactions",
    # schedule_interval="*/5 * * * *",
    catchup=False,
)

# Generate a unique folder name for this run based on trigger time
run_folder = "run_{{ ts_nodash }}"

# 1. Fetch Raw (Simulated by data generator)
fetch_raw = BashOperator(
    task_id="fetch_raw",
    bash_command=f"python3 /opt/airflow/spark_jobs/generate_data.py {run_folder}",
    dag=dag,
)

# 2. Ingest to Iceberg Raw
ingest = SparkSubmitOperator(
    task_id="ingest",
    application="/opt/airflow/spark_jobs/ingest.py",
    conn_id="spark_default",
    jars=ALL_JARS,
    application_args=["s3a://raw-transactions/*.csv", run_folder],
    dag=dag,
)

# 2b. Basic Cleansing
clean = SparkSubmitOperator(
    task_id="clean",
    application="/opt/airflow/spark_jobs/clean.py",
    conn_id="spark_default",
    jars=ALL_JARS,
    application_args=[run_folder],
    dag=dag,
)

# 3. Normalize
normalize = SparkSubmitOperator(
    task_id="normalize",
    application="/opt/airflow/spark_jobs/normalize.py",
    conn_id="spark_default",
    jars=ALL_JARS,
    application_args=[run_folder],
    dag=dag,
)

# 4. Filter Success
filter_success = SparkSubmitOperator(
    task_id="filter_success",
    application="/opt/airflow/spark_jobs/filter.py",
    conn_id="spark_default",
    jars=ALL_JARS,
    application_args=[run_folder],
    dag=dag,
)

# 5. Enrich
enrich = SparkSubmitOperator(
    task_id="enrich",
    application="/opt/airflow/spark_jobs/enrich.py",
    conn_id="spark_default",
    jars=ALL_JARS,
    application_args=[run_folder],
    dag=dag,
)

# 6. Aggregate
aggregate = SparkSubmitOperator(
    task_id="aggregate",
    application="/opt/airflow/spark_jobs/aggregate.py",
    conn_id="spark_default",
    jars=ALL_JARS,
    application_args=[run_folder],
    dag=dag,
)

# 7. Final Step (e.g. Health Check or Cleanup)
write_iceberg = PythonOperator(
    task_id="write_iceberg",
    python_callable=lambda: print(
        "ETL cycle completed successfully. Tables updated in Iceberg."
    ),
    dag=dag,
)

(
    fetch_raw
    >> ingest
    >> clean
    >> normalize
    >> filter_success
    >> enrich
    >> aggregate
    >> write_iceberg
)
