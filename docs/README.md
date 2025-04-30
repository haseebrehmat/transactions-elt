# 📖 Project Documentation Index

Welcome to the detailed guide for the Banking Transactions ETL project. This guide is broken down into easy-to-follow chapters.

### 🏁 Start Here
1.  [**Introduction**](01_introduction.md) - The big picture, the "why", and the goals.
2.  [**Infrastructure Overview**](02_infrastructure.md) - Docker, MinIO, Spark, and how the "team" works together.

### ⚙️ The Pipeline (Conceptual)
3.  [**Spark Jobs**](03_spark_jobs.md) - Detailed breakdown of the Python code that processes the data.
4.  [**Orchestration**](04_orchestration.md) - How Airflow acts as the brain of the operation.

### 📊 Frontend & Data
5.  [**Dashboard**](05_dashboard.md) - Visualizing the results with Streamlit.
6.  [**Apache Iceberg**](06_advanced_iceberg.md) - A deep dive into why we use Iceberg and its powerful features.

### 🔍 Code Deep Dives (Implementation Details)
7.  [**Deep Dive: Ingestion Code**](07_code_implementation_details.md) - Line-by-line breakdown of the `ingest_raw` implementation.
8.  [**Deep Dive: Common Utilities**](08_code_deep_dive_common.md) - Connections, Iceberg helpers, and snapshots.
9.  [**Deep Dive: Transformations**](09_code_deep_dive_spark_pipeline.md) - Cleaning, Normalization, Filtering, and Aggregation logic.
10. [**Deep Dive: Data Generation**](10_code_deep_dive_data_gen.md) - How we simulate raw banking records.
11. [**Deep Dive: Orchestration**](11_code_deep_dive_orchestration.md) - Airflow DAGs, Tasks, and Operators.
12. [**Deep Dive: Dashboard Code**](12_code_deep_dive_dashboard.md) - Building the UI and Analytics.
13. [**Deep Dive: Infrastructure**](13_infrastructure_deep_dive.md) - Docker Compose, Dockerfiles, and Port mapping.

---
*Created for beginners with Python and SQL knowledge who want to learn Data Engineering.*
