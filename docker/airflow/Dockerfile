FROM apache/airflow:2.7.2-python3.11

USER root
RUN apt-get update && \
    apt-get install -y --no-install-recommends openjdk-17-jdk procps && \
    apt-get autoremove -yqq --purge && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

USER airflow
# Dynamically find JAVA_HOME to support different architectures (arm64/amd64)
ENV JAVA_HOME=/usr/lib/jvm/default-java
USER root
RUN ln -s $(readlink -f /usr/bin/java | sed "s:bin/java::") /usr/lib/jvm/default-java

# Iceberg and AWS dependencies versions (matching Spark cluster)
ENV ICEBERG_VERSION=1.4.2
ENV AWS_SDK_VERSION=1.12.262
ENV HADOOP_AWS_VERSION=3.3.4
ENV SPARK_HOME=/home/airflow/.local/lib/python3.11/site-packages/pyspark

# Download JARs to a location Airflow can access
RUN mkdir -p /opt/airflow/jars && \
    curl -o /opt/airflow/jars/iceberg-spark-runtime-3.5_2.12-${ICEBERG_VERSION}.jar https://repo1.maven.org/maven2/org/apache/iceberg/iceberg-spark-runtime-3.5_2.12/${ICEBERG_VERSION}/iceberg-spark-runtime-3.5_2.12-${ICEBERG_VERSION}.jar && \
    curl -o /opt/airflow/jars/aws-java-sdk-bundle-${AWS_SDK_VERSION}.jar https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-bundle/${AWS_SDK_VERSION}/aws-java-sdk-bundle-${AWS_SDK_VERSION}.jar && \
    curl -o /opt/airflow/jars/hadoop-aws-${HADOOP_AWS_VERSION}.jar https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/${HADOOP_AWS_VERSION}/hadoop-aws-${HADOOP_AWS_VERSION}.jar

USER airflow
RUN --mount=type=cache,target=/home/airflow/.cache/pip \
    pip install --default-timeout=1000 apache-airflow-providers-apache-spark==4.2.0 pyspark==3.5.0 faker==20.0.0 boto3==1.28.0
