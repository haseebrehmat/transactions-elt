import csv
import random
import uuid
from datetime import datetime, timedelta
import boto3
import os


def generate_transactions(num_rows=100):
    statuses = ["SUCCESS", "SUCCESS", "SUCCESS", "SUCCESS", "FAILED", "PENDING"]
    types = ["TRANSFER", "WITHDRAWAL", "DEPOSIT", "PAYMENT"]
    currencies = ["USD", "EUR", "GBP", "INR"]
    channels = ["MOBILE", "WEB", "ATM", "BRANCH"]

    rows = []
    base_time = datetime.now()

    for _ in range(num_rows):
        rows.append(
            {
                "txn_id": str(uuid.uuid4()),
                "customer_id": f"CUST_{random.randint(1000, 9999)}",
                "txn_amount": round(random.uniform(10.0, 50000.0), 2),
                "txn_date": (
                    base_time - timedelta(minutes=random.randint(0, 5))
                ).strftime("%Y-%m-%d %H:%M:%S"),
                "txn_type": random.choice(types),
                "status": random.choice(statuses),
                "currency": random.choice(currencies),
                "channel": random.choice(channels),
            }
        )
    return rows


import sys


def upload_to_minio(data, filename, execution_folder=None):
    s3 = boto3.client(
        "s3",
        endpoint_url=os.getenv("MINIO_ENDPOINT", "http://minio:9000"),
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID", "admin"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY", "password123"),
        region_name="us-east-1",
    )

    # 1. Upload to raw-transactions (Source for Spark)
    bucket = "raw-transactions"
    try:
        s3.create_bucket(Bucket=bucket)
    except:
        pass

    local_path = f"/tmp/{filename}"
    with open(local_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

    s3.upload_file(local_path, bucket, filename)
    print(f"Uploaded {filename} to {bucket}")

    # 2. Upload to pipeline-runs (Observability)
    runs_bucket = "pipeline-runs"
    iceberg_bucket = "iceberg-warehouse"

    for b in [runs_bucket, iceberg_bucket]:
        try:
            s3.create_bucket(Bucket=b)
        except:
            pass

    if execution_folder:
        # In pipeline-runs, we save it in the run folder as 0_extraction
        s3_key = f"{execution_folder}/0_extraction/{filename}"
        s3.upload_file(local_path, runs_bucket, s3_key)
        print(f"Uploaded extraction snapshot to: {runs_bucket}/{s3_key}")


if __name__ == "__main__":
    now_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"transactions_{now_str}.csv"
    data = generate_transactions(150)

    # Check if execution folder is passed from Airflow
    execution_folder = sys.argv[1] if len(sys.argv) > 1 else None
    upload_to_minio(data, filename, execution_folder)
