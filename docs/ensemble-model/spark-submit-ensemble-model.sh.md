# `spark-submit-ensemble-model.sh`

This document explains the spark-submit script used to submit the PySpark job (`ensemble-model.py`) to a Spark cluster from within a Docker container running in Kubernetes.
The script configures and launches a Spark application with specific resource allocations, network configurations, and dependencies.

## Usage

To use this script:

1. Ensure the script has execute permissions:
   ```bash
   chmod +x spark-submit-ensemble-model.sh
   ```

2. The script should be placed in the Docker container at build time

3. The script can be executed directly:
   ```bash
   ./spark-submit-ensemble-model.sh
   ```

4. Alternatively, it can be specified as the container's entrypoint in the Dockerfile:
   ```dockerfile
   ENTRYPOINT ["/app/spark-submit-ensemble-model.sh"]
   ```

## Script
### Cluster Configuration

```bash
#!/bin/bash
/opt/bitnami/spark/bin/spark-submit \
    --master spark://spark-master-service:7077 \
    --deploy-mode client \
    --name "EnsembleModel" \
```

This section defines the basic Spark cluster configuration:
- Uses the Bitnami Spark distribution's spark-submit command
- Specifies the Spark master URL (`spark://spark-master-service:7077`)
- Sets deploy mode to `client` (driver runs in the submitting process)
- Names the application "EnsembleModel" for identification in the Spark UI

### Package Dependencies

```bash
    --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.4 \
```

This section specifies required external dependencies:
- Includes the Spark-Kafka integration package
- Uses version 3.5.4 of the package
- Compatible with Scala 2.12
- Enables Spark to read from and write to Kafka topics

### Resource Allocation

```bash
    --driver-memory 1g \
    --conf spark.driver.maxResultSize=1g \
    --executor-cores 1 \
    --executor-memory 1g \
    --total-executor-cores 1 \
```

This section configures the computational resources:
- Driver memory: 1GB
- Maximum result size for driver: 1GB
- Cores per executor: 1
- Memory per executor: 1GB
- Total cores across all executors: 1
- These settings are optimized for a small-scale deployment

### Driver Configuration

```bash
    --conf spark.executor.instances=1 \
    --conf spark.driver.bindAddress=0.0.0.0 \
    --conf spark.driver.host=ensemble-model-service \
    --conf spark.driver.port=7072 \
    --conf spark.driver.blockManager.port=35635 \
```

This section sets up the Spark driver networking:
- Number of executor instances: 1
- Driver bind address: 0.0.0.0 (accepts connections from any IP)
- Driver hostname: ensemble-model-service (matches Kubernetes service name)
- Driver port: 7072 (for Spark driver communications)
- Block manager port: 35635 (for data block management)
- These settings ensure proper communication within the Kubernetes cluster

### Application Specification

```bash
    /app/ensemble-model.py
```

This final line specifies:
- The path to the PySpark application file
- Located at `/app/ensemble-model.py` within the container
- This is the main application that will be executed by Spark
