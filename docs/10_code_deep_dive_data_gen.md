# 10 - Code Deep Dive: Data Generation (`generate_data.py`)

This script does not use Spark. Instead, it uses standard Python to simulate a stream of incoming transactions. It acts as our "Source System."

---

## **1. `generate_transactions(num_rows=100)`**

### **Logic**
- **Libraries**: Uses `uuid` for IDs and `random` for values.
- **Lists**: Defines standard banks categories like `statuses`, `types`, `currencies`, and `channels`.
- **Loop**: Creates a list of dictionaries. Each dictionary represents one transaction row.
- **Output**: Returns a list of 100-150 transaction objects.

---

## **2. `upload_to_minio(data, filename, execution_folder)`**

This is the bridge between our local script and the "Cloud" (MinIO).

### **Key Implementation Details**
- **`boto3.client("s3", ...)`**: This is the official Amazon library for talking to S3. We point it to our local `minio` container.
- **Bucket Creation**:
    - `s3.create_bucket(...)`: Checks if `raw-transactions` and `pipeline-runs` exist. If not, it creates them.
- **Local to Remote**:
    - **Stage 1**: It writes the generated data to a temporary file in `/tmp/`.
    - **Stage 2**: It uploads that file to the `raw-transactions` bucket. This simulates a bank "dropping" a file into our system.
    - **Stage 3 (Observability)**: It uploads a second copy to the `pipeline-runs` folder as `0_extraction`. 

---

## **3. Main Execution Block**
```python
if __name__ == "__main__":
    now_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"transactions_{now_str}.csv"
    data = generate_transactions(150)
    
    execution_folder = sys.argv[1] # Received from Airflow
    upload_to_minio(data, filename, execution_folder)
```
- **File Naming**: Uses a timestamp in the filename (e.g., `transactions_20260104_120000.csv`) so that multiple runs don't overwrite each other in the "Raw" bucket.
- **System Arguments**: It listens for the `execution_folder` name passed by Airflow's BashOperator.
