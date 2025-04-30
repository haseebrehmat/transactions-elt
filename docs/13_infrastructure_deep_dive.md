# 13 - Infrastructure Deep Dive: Docker & Compose

This project uses **Docker Compose** to run 7 different software systems on a single laptop as if they were in a professional data center.

---

## **1. The Core Infrastructure (`docker-compose.yaml`)**

### **Service Networking**
Every service is joined to a network called `etl_network`. This allows `airflow` to reach `spark-master` simply by using the name "spark-master."

### **Service Volumes (The "Shared Folders")**
- `./spark_jobs:/opt/airflow/spark_jobs`: This is crucial. It shares the Python files on your computer with the Airflow and Spark containers. When you edit a script, the container sees the change instantly!
- `./data/minio:/data`: Ensures that if you stop the project, your transactions and Iceberg tables aren't deleted.

### **The Initialization Logic (`airflow-init`)**
This is a "Run and Done" service.
1.  **`airflow db migrate`**: Sets up the Postgres database for Airflow.
2.  **`airflow users create`**: Creates the `admin/admin` login.
3.  **Connection Setup**: It automatically runs `airflow connections add` to pre-configure the Spark connection (`spark_default`). This saves you from having to set it up manually.

---

## **2. Specialized Dockerfiles**

### **Spark Dockerfile (`docker/spark/Dockerfile`)**
- **Base**: Uses Bitnami's Spark image (Industry Standard).
- **Customization**:
    - We use `curl` to download specific **JAR files** (Java Archive). 
    - `iceberg-spark-runtime`: Teaches Spark the Iceberg language.
    - `hadoop-aws` & `aws-java-sdk`: Teach Spark how to talk to S3/MinIO.

### **Airflow Dockerfile (`docker/airflow/Dockerfile`)**
- **Base**: Apache Airflow official image.
- **Customization**:
    - Installs **Java** (`openjdk-17-jre`). Airflow needs Java because it uses the "Spark Submit" tool, which is a Java application.
    - Installs `requirements.txt` which includes `pyspark`, `boto3`, and `pandas`.

---

## **3. Summary of Ports (The "Doors")**

| Service | Port | What happens here? |
| :--- | :--- | :--- |
| **Airflow** | `8081` | Trigger and monitor your pipeline. |
| **MinIO** | `9001` | Browse the "buckets" and see the actual CSV/Iceberg files. |
| **Spark Master** | `8080` | See if your workers are alive and check current job progress. |
| **Spark Driver** | `4040` | High-detail logs of a *running* job (Active only during a task). |
| **Dashboard** | `8501` | The final analytics interface. |

---
## **Conclusion**
You now have a 100% comprehensive map of how every line of code and every configuration relates to the project. From a `random.randint` in a Python script to a Docker port mapping!
