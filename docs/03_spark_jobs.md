# 03 - Spark Jobs (The Processing Logic)

This is where the magic happens! We have several Python scripts in the `spark_jobs/` folder. Each one performs a specific transformation.

## 1. `common.py` (The Utility Belt)
Before we start, we need a setup. Every Spark job needs a "SparkSession."
```python
def get_spark_session(app_name):
    # This sets up connection to MinIO and Iceberg
    return SparkSession.builder.appName(app_name)...getOrCreate()
```
It also contains `write_iceberg_table`, which handles the logic of "Does this table exist? If no, create it. If yes, add data to it."

## 2. `ingest.py` (The Receptionist)
- **What it does**: Reads raw `.csv` files from the `raw-transactions` bucket.
- **Key Move**: It adds an `ingestion_date` column so we know *when* we received the data.
- **Storage**: Saves it into the `iceberg.bank.raw_transactions` table.

## 3. `clean.py` (The Janitor)
- **What it does**: Real data has "Nulls" (empty values). This script drops rows where crucial info (like `txn_id`) is missing.
- **Standardization**: It converts text to `UPPERCASE` so that "transfer" and "TRANSFER" are treated the same way.

## 4. `normalize.py` (The Translator)
- **What it does**: CSVs treat everything like text. We need numbers to be **Decimals** (for money) and dates to be **Timestamps**.
- **Transformation**: `col("txn_amount").cast("decimal(18,2)")`.

## 5. `filter.py` (The Security Guard)
- **What it does**: We only want to analyze successful transactions.
- **Logic**: `df.filter(col("status") != "FAILED")`.

## 6. `enrich.py` (The Analyst)
- **What it does**: Adds "Value Added" columns.
- **Example**: It creates a flag `is_high_value` which is `True` if the transaction is over $10,000. This makes it easy for the dashboard to highlight big spenders.

## 7. `aggregate.py` (The Accountant)
- **What it does**: Instead of looking at every single transaction, it sums them up per customer, per day.
- **Result**: You get a table with columns like `total_amount` and `total_txns`.

---
**Next Step:** [Understanding Orchestration with Airflow](04_orchestration.md)
