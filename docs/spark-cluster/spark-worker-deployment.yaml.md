# Spark Worker Kubernetes Deployment Documentation

This configuration file defines the deployment for Spark worker nodes in a Kubernetes cluster. Spark workers are responsible for executing tasks assigned by the Spark master node and performing the actual data processing work. This deployment uses a custom Spark Docker image defined in `./src/spark-cluster/Dockerfile`.

## Usage

To deploy the Spark workers:

1. Ensure your Kubernetes cluster is running
2. Verify the Spark master deployment is active
3. Make sure the `custom-spark:latest` image is available
4. Apply the configuration:
   ```bash
   kubectl apply -f spark-worker-deployment.yaml
   ```
5. Verify the deployment:
   ```bash
   kubectl get deployments
   kubectl get pods
   ```

### Resource Considerations

This configuration allocates:
- 2GB memory per worker
- 2 CPU cores per worker
- Total cluster resources: 4GB memory and 4 CPU cores (2 workers)

Adjust these values based on your cluster's available resources and workload requirements.

### Scaling

To scale the number of workers:
```bash
kubectl scale deployment spark-worker --replicas=3
```

Ensure your Kubernetes cluster has sufficient resources before scaling.


## Deployment Configuration

### Basic Metadata

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: spark-worker
```

This section defines:
- API version: `apps/v1` for Deployment resources
- Resource type: `Deployment`
- Deployment name: `spark-worker`

### Replica and Selector Configuration

```yaml
spec:
  replicas: 2
  selector:
    matchLabels:
      app: spark-worker
  template:
    metadata:
      labels:
        app: spark-worker
```

This section specifies:
- Number of replicas: 2 (two worker nodes)
- Label selector for identifying worker pods
- Pod template metadata with matching labels
- Ensures multiple workers are available for distributed processing

### Container Specification

```yaml
  template:
    metadata:
      labels:
        app: spark-worker
    spec:
      containers:
        - name: spark-worker
          image: custom-spark:latest
          imagePullPolicy: IfNotPresent
          env:
            - name: SPARK_MODE
              value: worker
            - name: SPARK_MASTER_URL
              value: spark://spark-master-service:7077
            - name: SPARK_WORKER_MEMORY
              value: 2G
            - name: SPARK_WORKER_CORES
              value: '2'
            - name: SPARK_RPC_AUTHENTICATION_ENABLED
              value: 'no'
            - name: SPARK_RPC_ENCRYPTION_ENABLED
              value: 'no'
            - name: SPARK_SSL_ENABLED
              value: 'no'
            - name: SPARK_LOCAL_STORAGE_ENCRYPTION_ENABLED
              value: 'no'
```

This section defines:

Container Configuration:
- Name: `spark-worker`
- Image: `custom-spark:latest`
- Image pull policy: `IfNotPresent` (uses local image if available)

Environment Variables:
- `SPARK_MODE`: Set to "worker" for worker node configuration
- `SPARK_MASTER_URL`: Points to the Spark master service at `spark://spark-master-service:7077`
- Resource allocation:
  - Memory: 2GB per worker (`SPARK_WORKER_MEMORY`)
  - CPU cores: 2 cores per worker (`SPARK_WORKER_CORES`)
- Security settings (all disabled for development):
  - RPC authentication
  - RPC encryption
  - SSL
  - Local storage encryption