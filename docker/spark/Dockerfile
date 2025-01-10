FROM bitnamilegacy/spark:3.5.0

USER root

# Install tools
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Iceberg and AWS dependencies versions
ENV ICEBERG_VERSION=1.4.2
ENV AWS_SDK_VERSION=1.12.262
ENV HADOOP_AWS_VERSION=3.3.4

# Download Iceberg and AWS JARs
RUN curl -o /opt/bitnami/spark/jars/iceberg-spark-runtime-3.5_2.12-${ICEBERG_VERSION}.jar https://repo1.maven.org/maven2/org/apache/iceberg/iceberg-spark-runtime-3.5_2.12/${ICEBERG_VERSION}/iceberg-spark-runtime-3.5_2.12-${ICEBERG_VERSION}.jar && \
    curl -o /opt/bitnami/spark/jars/aws-java-sdk-bundle-${AWS_SDK_VERSION}.jar https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-bundle/${AWS_SDK_VERSION}/aws-java-sdk-bundle-${AWS_SDK_VERSION}.jar && \
    curl -o /opt/bitnami/spark/jars/hadoop-aws-${HADOOP_AWS_VERSION}.jar https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/${HADOOP_AWS_VERSION}/hadoop-aws-${HADOOP_AWS_VERSION}.jar

# Install Python dependencies for processing/generation
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --default-timeout=100 faker==20.0.0 boto3==1.28.0 pandas==2.1.0 pyarrow==13.0.0

USER 1001
