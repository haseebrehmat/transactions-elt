# 🏦 Banking Sentinel: Distributed Transaction Ledger

Building a high-performance, fault-tolerant financial ETL ecosystem using **Apache Spark**, **Apache Iceberg**, and **Airflow**.

---

## **🌟 Architectural Overview**

Banking Sentinel is a mission-critical transaction processing engine designed to transform chaotic raw banking streams into structured, actionable financial intelligence. It leverages a modern **Lakehouse Architecture** to provide ACID compliance and sub-second analytical capabilities.

### **Core Technology Stack**
- **💻 Processing Engine:** PySpark 3.5.0 (Distributed Analytics)
- **🧊 Table Format:** Apache Iceberg (ACID Compliance, Time-Travel, Schema Evolution)
- **🎼 Orchestration:** Apache Airflow (Directed Acyclic Graph Management)
- **☁️ Object Storage:** Minio (S3-Compatible High-Availability Storage)
- **📊 Analytics UX:** Streamlit "Premium Sentinel" Dashboard
- **🐳 Infrastructure:** Dockerized Microservices Architecture

---

## **🔄 Multi-Stage Pipeline Architecture**

The pipeline is structured into **seven discrete stages**, each ensuring data integrity and observability via stage-wise persistent snapshots.

1.  **📥 EXTRACTION**: Synthesize high-entropy banking transactions (txn_id, customer_id, various metadata).
2.  **📦 RAW INGESTION**: Landing zone with idempotent writing to the `iceberg.bank.raw_transactions` table.
3.  **🧹 BASIC CLEANSING**: Removal of non-conforming records and whitespace sanitization.
4.  **⚙️ NORMALIZATION**: Precision casting of decimal values and standardized ISO timestamp parsing.
5.  **🔍 SUCCESS ONLY**: High-speed filtering of terminal transaction states.
6.  **💎 FEATURE ENRICHMENT**: Derived signal engineering (e.g., `is_high_value` detection).
7.  **📈 DAILY AGGREGATION**: Final analytical ledger with customer-centric metrics.

---

## **⚡ Operational Excellence**

### **1. Rapid Deployment**
Spin up the entire financial ecosystem in minutes:
```bash
docker-compose up -d
```

### **2. Sentinel Control Center (Dashboard)**
Access the **Premium Sentinel Dashboard** at `http://localhost:8501`. 
- **Dark-Theme Optimized Interface**: High-contrast, accessibility-focused design.
- **Full-Spectrum Observability**: Toggle between all 7 pipeline stages with instant data previews.
- **Executive Analytics**: Real-time visualization of transaction volume and customer activity.
- **Performance Heartbeat**: Real-time sync status and system health monitoring.

---

## **🛠 Infrastructure Access**

| Service | Endpoint | Default Credentials |
| :--- | :--- | :--- |
| **Airflow Sentinel** | `http://localhost:8081` | `admin / admin` |
| **Sentinel Dashboard** | `http://localhost:8501` | *N/A (Public)* |
| **MinIO Deep Storage** | `http://localhost:9001` | `admin / password123` |
| **Spark Master** | `http://localhost:8080` | *N/A (Public)* |

---

## **🏗 Engineering Best Practices Implemented**

- **Centralized Write Helpers**: A unified writing interface in `common.py` that handles table creation vs. appending automatically using Spark V2 APIs.
- **Idempotency**: All jobs can be re-run safely without duplicating data, thanks to rigorous Iceberg naming and namespace (`iceberg.bank`) management.
- **Horizontal Scalability**: Designed to run across a distributed Spark cluster for PB-level transaction streams.
- **Atomic Commits**: Project history maintained with professional, assertive commit strategies.

---

## **📂 Repository Blueprint**

- `/dags`: Pipeline orchestration logic.
- `/spark_jobs`: Core processing kernels and synthetic data generators.
- `/dashboard`: Premium Streamlit UI application.
- `/docker`: Specialized container definitions for Spark and Airflow.
- `/scripts`: Support utilities for data validation.

---
*Created with focus on Reliability, Scalability, and Visual Excellence.*
