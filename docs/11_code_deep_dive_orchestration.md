# 11 - Code Deep Dive: Orchestration (`transaction_etl_dag.py`)

The DAG file defines the roadmap for our data. It doesn't process data itself; it tells other tools *what* to process.

---

## **1. DAG Configuration**
```python
default_args = {
    "owner": "antigravity",
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}
```
- **`owner`**: Helpful in large teams to see who "owns" any failures.
- **`retries`**: If a job fails (maybe Spark cluster was too busy), Airflow will automaticall wait 5 minutes and try again.

---

## **2. Dynamic Variables**
```python
run_folder = "run_{{ ts_nodash }}"
```
- **Jinja Templating**: The `{{ ts_nodash }}` is a special Airflow variable. When the DAG runs at 10:00 AM, it becomes `20260104100000`. 
- **Consistency**: We pass this `run_folder` to *every* task. This is the "Thread" that ties all snapshots in MinIO together.

---

## **3. The Operators (The Workers)**

### **BashOperator (`fetch_raw`)**
- **Action**: Runs a standard terminal command: `python3 /opt/airflow/spark_jobs/generate_data.py`.
- **Reason**: We don't need the power of Spark to generate 150 rows. A simple Python script is faster.

### **SparkSubmitOperator (Everything else)**
- **`task_id`**: The name shown in the Airflow UI.
- **`application`**: The path to the Python script inside the container.
- **`conn_id`**: Points to `spark_default`. This is where Airflow finds the URL for the Spark Master.
- **`jars`**: We pass the Iceberg and AWS JAR files. Spark needs these Java libraries to handle S3 connections and Iceberg table logic.
- **`application_args`**: We pass the `run_folder` so the script knows where to save its snapshots.

---

## **4. DAG Structure (The Workflow)**
```python
fetch_raw >> ingest >> clean >> normalize >> filter_success >> enrich >> aggregate >> write_iceberg
```
- This line sets the **lineage**. 
- If `clean` fails, Airflow will **stop** the pipeline and won't attempt `normalize`. This prevents our "Cleaned" or "Aggregated" tables from containing broken data.
