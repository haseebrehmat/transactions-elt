# 04 - Orchestration (The Brain)

Even with great Spark jobs, we need something to run them in the right order. That's what **Apache Airflow** is for.

## What is a DAG?
DAG stands for **Directed Acyclic Graph**. 
- **Directed**: It has a flow (A -> B -> C).
- **Acyclic**: It can't go in circles (no infinite loops).
- **Graph**: It's a map of tasks.

## Our Pipeline (`transaction_etl_dag.py`)

In Airflow, we define "Tasks." Our tasks are mostly **SparkSubmitOperators**. This is a special tool that tells the Spark Cluster: "Hey! Run this specific Python file with these settings."

### Task Dependencies
We use the `>>` symbol to set the order:
```python
fetch_raw >> ingest >> clean >> normalize >> filter_success >> enrich >> aggregate >> write_iceberg
```

### Why use Airflow?
1.  **Retries**: If a Spark job fails because of a network glitch, Airflow can automatically try it again 5 minutes later.
2.  **Scheduling**: We can set this to run every hour, every day, or every Monday at 2 AM.
3.  **Visibility**: If something breaks, the Airflow UI turns that task **Red**, and we can click it to see the error logs immediately.
4.  **Parallelism**: If we had two independent tasks, Airflow could run them at the same time to save time.

---
**Next Step:** [Visualizing with the Dashboard](05_dashboard.md)
