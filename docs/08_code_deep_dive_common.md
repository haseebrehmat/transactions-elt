# 08 - Code Deep Dive: `common.py` (The Shared Foundation)

The `common.py` file is the heart of the project. It contains the logic that almost every other Spark job uses. By centralizing this code, we ensure that every job connects to the database and storage in the exact same way.

---

## **1. `get_spark_session(app_name)`**

This function builds the "Engine" (SparkSession) for each job.

### **Parameters**
- **`app_name` (string)**: The name that will show up in the Spark UI (e.g., "T1 - Raw Ingestion").

### **Key Implementation Details**
- **Environment Variables**:
    - `aws_access_key` / `aws_secret_key`: Used to log into MinIO.
    - `minio_endpoint`: The URL where our storage is located (`http://minio:9000`).
- **Iceberg Configuration**:
    - `spark.sql.extensions`: Tells Spark to use Iceberg's special SQL features.
    - `spark.sql.catalog.iceberg`: Defines our catalog (where tables are tracked). We use a `hadoop` type catalog.
    - `spark.sql.catalog.iceberg.warehouse`: Points to `s3a://iceberg-warehouse/` where the actual data files will live.
- **S3 (MinIO) Configuration**:
    - `fs.s3a.impl`: Tells Spark to use the Hadoop S3A library to talk to S3.
    - `fs.s3a.path.style.access`: Set to `true` because MinIO uses a specific URL format.
- **Namespace Setup**:
    - `spark.sql("CREATE NAMESPACE IF NOT EXISTS iceberg.bank")`: This is like creating a folder or a database schema called `bank` inside our Iceberg catalog.

---

## **2. `write_stage_snapshot(df, execution_folder, stage_name)`**

This function saves a "checkpoint" of the data for debugging.

### **Parameters**
- **`df` (DataFrame)**: The Spark table you want to save.
- **`execution_folder` (string)**: The unique ID for the current run.
- **`stage_name` (string)**: The name of the step (e.g., `2_basic_cleansing`).

### **Key Implementation Details**
- **`df.coalesce(1)`**: This is a performance trick. It tells Spark to combine all data into one single file. This is fine for our small dataset and makes it much easier for the Dashboard to read.
- **`.write.mode("overwrite")`**: If we run the same step twice, it will replace the old snapshot with the new one.
- **`.csv(output_path)`**: Saves the data as a simple CSV file in the `pipeline-runs` bucket.

---

## **3. `write_iceberg_table(df, table_name, mode="append")`**

This is a "Smart Writer" that handles the complexity of Iceberg's Spark V2 API.

### **Parameters**
- **`df` (DataFrame)**: The data to save.
- **`table_name` (string)**: The name of the table in the `bank` namespace.
- **`mode` (string)**: Either `"append"` (add to existing) or `"overwrite"` (replace everything).

### **Key Implementation Details**
- **Table Existence Check**:
    - `spark.catalog.tableExists(full_table_name)`: Before writing, Spark checks if the table already exists in the catalog.
- **Logical Flow**:
    - If **Overwrite**: Uses `.createOrReplace()`, which handles everything in one atomic transaction.
    - If **Append**:
        - If the table exists: Uses `.append()`.
        - If the table is brand new: Uses `.create()`.
- **Portability**: By using `df.sparkSession`, the function "steals" the configuration from whatever DataFrame is passed to it, so it doesn't need to create its own connection.
