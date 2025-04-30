# 07 - Code Implementation: Deep Dive into `ingest_raw`

In this chapter, we go beyond the "what" and look exactly at the "how." We will dissect the primary method in the `ingest.py` script to understand the actual code lines that move your data.

## **Method Profile: `ingest_raw`**

This method is the "Front Door" of the ETL pipeline. It is responsible for taking raw CSV data from storage and putting it into our high-performance Iceberg table.

### **Function Signature**
```python
def ingest_raw(input_path, execution_folder):
```

### **Parameters**
1.  **`input_path`**: A string containing the S3 path where the raw CSVs are located (e.g., `s3a://raw-transactions/*.csv`).
2.  **`execution_folder`**: A unique ID for the current pipeline run (passed from Airflow), used to save snapshots for debugging.

---

## **Step-by-Step Breakdown**

### **1. Creating the Spark Session**
```python
spark = get_spark_session("T1 - Raw Ingestion")
```
- **What happens**: This calls our helper in `common.py`.
- **Key Point**: It doesn't just "start Spark." It configures the **Iceberg Extensions** and connects Spark to our **MinIO S3** storage using your access keys. Without this configuration, Spark wouldn't know how to speak to the "Lakehouse."

### **2. Reading the Raw Data**
```python
df_raw = (
    spark.read.option("header", "true")
    .option("inferSchema", "true")
    .csv(input_path)
)
```
- **`header=true`**: Tells Spark the first line of the file is the names of the columns (like `txn_id`).
- **`inferSchema=true`**: This is a powerful feature where Spark reads a few lines and "guesses" the data types (e.g., it sees numbers and decides that column should be an Integer).
- **Result**: Data is loaded into a **DataFrame** (`df_raw`), which is basically a giant table in Spark's memory.

### **3. The Debug Snapshot**
```python
write_stage_snapshot(df_raw, execution_folder, "1_raw_ingestion")
```
- **Purpose**: We save a physical copy of what we just read into a folder called `1_raw_ingestion`. 
- **Why?**: If the pipeline breaks later, you can look at this CSV file to see exactly what Spark saw at the very beginning.

### **4. Adding Metadata**
```python
df_raw = df_raw.withColumn("ingestion_date", current_date())
```
- **Implementation**: We use `withColumn` to add a brand new column that didn't exist in the CSV.
- **Value**: It records the exact date this data entered our system. This is a common practice in Professional Data Engineering to help with auditing.

### **5. Writing to Apache Iceberg**
```python
write_iceberg_table(df_raw, "raw_transactions", mode="overwrite")
```
- **`write_iceberg_table`**: This is our smart helper. Under the hood, it uses the **Spark V2 API** (`writeTo`).
- **`mode="overwrite"`**: Since we are reading *all* files from the raw bucket, we overwrite the target table to ensure we have a fresh, clean landing of current data.
- **Key Fact**: Because we use Iceberg, this "overwrite" is **atomic**. If the power goes out mid-save, the old data stays safe. Only a 100% successful save will update the table.

### **6. Cleanup**
```python
spark.stop()
```
- **Why?**: It releases the memory and resources back to the cluster. This is like turning off the lights when you leave a room.

---
**Next Step:** Review the logic in [03 - Spark Jobs](03_spark_jobs.md) for the "Clean" and "Normalize" stages.
