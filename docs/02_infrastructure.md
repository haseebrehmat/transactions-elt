# 02 - The Infrastructure (Under the Hood)

To run this project, we use **Docker**. Think of Docker as a way to package a computer inside a "container" so it runs exactly the same on your machine as it does on mine.

## Our Services (The "Team")

In our `docker-compose.yaml` file, we define several services:

### 1. MinIO (The Storage)
- **Role**: This is where our data "lives."
- **Analogy**: Think of it like a giant hard drive in the cloud.
- **Cool Fact**: It speaks the "S3 Language," which is the industry standard for storing files.

### 2. Spark (The Muscle)
- **Role**: The processing engine.
- **Master vs. Worker**:
    - The **Master** is the boss. It plans the work.
    - The **Worker** does the actual math. If we had a billion rows, we could just add more workers!

### 3. Airflow (The Conductor)
- **Role**: It tells everyone when to start and what to do next.
- **Webserver**: The UI where you see the "boxes and lines" (DAGs).
- **Scheduler**: The background process that monitors timers and dependencies.

### 4. Postgres (The Memory)
- **Role**: Airflow needs a place to remember which tasks finished and which failed. It stores that metadata here.

### 5. Dashboard (The Face)
- **Role**: This is our custom Streamlit app that reads data from MinIO and shows it to you in pretty graphs.

## How they talk to each other
Docker creates a private "network."
- Instead of using complicated IP addresses, they use names.
- Airflow talks to Spark at `spark://spark-master:7077`.
- Everyone talks to MinIO at `http://minio:9000`.

---
**Next Step:** [Diving into Spark Jobs](03_spark_jobs.md)
