import boto3
import pandas as pd
import io
import os
import sys


def get_s3_client():
    return boto3.client(
        "s3",
        endpoint_url=os.getenv("MINIO_ENDPOINT", "http://localhost:9000"),
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID", "admin"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY", "password123"),
        region_name="us-east-1",
    )


def list_recent_runs():
    s3 = get_s3_client()
    bucket = "pipeline-runs"

    try:
        response = s3.list_objects_v2(Bucket=bucket, Delimiter="/")
        if "CommonPrefixes" not in response:
            print("No runs found in pipeline-runs bucket.")
            return []

        runs = [p["Prefix"].strip("/") for p in response["CommonPrefixes"]]
        return sorted(runs, reverse=True)
    except Exception as e:
        print(f"Error listing runs: {e}")
        return []


def read_stage_data(run_folder, stage_name):
    s3 = get_s3_client()
    bucket = "pipeline-runs"
    prefix = f"{run_folder}/{stage_name}/"

    try:
        # Find the CSV file in the folder (Spark saves it as part-xxxx.csv)
        response = s3.list_objects_v2(Bucket=bucket, Prefix=prefix)
        if "Contents" not in response:
            print(f"No data found for stage {stage_name} in {run_folder}")
            return None

        csv_file = next(
            (obj["Key"] for obj in response["Contents"] if obj["Key"].endswith(".csv")),
            None,
        )
        if not csv_file:
            print(f"No CSV found in {prefix}")
            return None

        obj = s3.get_object(Bucket=bucket, Key=csv_file)
        df = pd.read_csv(io.BytesIO(obj["Body"].read()))
        return df
    except Exception as e:
        print(f"Error reading data: {e}")
        return None


def main():
    runs = list_recent_runs()
    if not runs:
        sys.exit(1)

    print("\nAvailable Pipeline Runs:")
    for i, run in enumerate(runs[:5]):
        print(f"{i+1}. {run}")

    selected_run = runs[0]
    print(f"\n--- Analysis for Latest Run: {selected_run} ---")

    stages = [
        ("0_extraction", "Raw Extracted Data"),
        ("6_daily_aggregation", "Final Daily Aggregation Summary"),
    ]

    for stage_id, title in stages:
        print(f"\n[ {title} ]")
        df = read_stage_data(selected_run, stage_id)
        if df is not None:
            print(f"Total Rows: {len(df)}")
            print(df.head(10).to_string(index=False))
        else:
            print("Stage data not available yet.")


if __name__ == "__main__":
    main()
