# 01 - Introduction to Banking Sentinel

Welcome to the **Banking Sentinel** documentation! This project is designed to show you how modern data engineering works in the real world.

## What is this project?
Imagine a bank where thousands of transactions happen every minute. We need a way to:
1.  **Collect** those transactions (Extraction).
2.  **Save** them securely (Ingestion).
3.  **Clean** them up because real-world data is often messy (Cleansing).
4.  **Analyze** them to find patterns, like how much money customers are spending daily (Aggregation).

## The "Data Lakehouse" Concept
You might know about **Databases** (SQL) and **Data Lakes** (storing files like CSVs). 
A **Data Lakehouse** (like the one we built here) combines both!
- We store data in files (for scale).
- We use **Apache Iceberg** to act like a database layer on top of those files. This lets us use SQL features like "Transactions" and "Schema Evolution" on simple files.

## High-Level Workflow
Our pipeline follows these steps:
1.  **Generate Data**: We create "fake" transactions to simulate a real bank.
2.  **Move to Storage**: We upload these files to **MinIO** (which works exactly like Amazon S3).
3.  **Process with Spark**: We use **PySpark** (Python + Spark) to do the heavy lifting. Spark is great because it can process millions of rows by splitting the work across many computers.
4.  **Orchestrate with Airflow**: We use **Airflow** as the "Brain" or the "Conductor" to make sure each step happens in the right order.
5.  **Visualize**: Finally, we show the results in a beautiful **Streamlit** dashboard.

---
**Next Step:** [Learn about the Infrastructure (Docker)](02_infrastructure.md)
