# `spark-master-deployment.yaml`

This configuration file defines the deployment and service for a Spark master node in a Kubernetes cluster. The Spark master is responsible for coordinating and managing Spark worker nodes and applications. It serves as the central coordination point for distributed processing in a Spark cluster.

## Usage

To deploy the Spark master:

1. Ensure your Kubernetes cluster is running
2. Make sure the `custom-spark:latest` image is available
3. Apply the configuration:
   ```bash
   kubectl apply -f spark-master-deployment.yaml
   ```
4. Verify the deployment:
   ```bash
   kubectl get deployments
   kubectl get pods
   kubectl get services
   ```

## Deployment Configuration

### Basic Metadata

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: spark-master
```

This section defines:
- API version: `apps/v1` for Deployment resources
- Resource type: `Deployment`
- Deployment name: `spark-master`

### Replica and Selector Configuration

```yaml
spec:
  replicas: 1
  selector:
    matchLabels:
      app: spark-master
  template:
    metadata:
      labels:
        app: spark-master
```

This section specifies:
- Number of replicas: 1 (single master node)
- Label selector for identifying pods
- Pod template metadata with matching labels
- Ensures high availability while maintaining only one active master

### Container Specification

```yaml
    spec:
      containers:
        - name: spark-master
          image: custom-spark:latest
          imagePullPolicy: IfNotPresent
          ports:
            - containerPort: 7077
              name: rpc
            - containerPort: 8080
              name: webui
          env:
            - name: SPARK_MODE
              value: master
            - name: SPARK_RPC_AUTHENTICATION_ENABLED
              value: 'no'
            - name: SPARK_RPC_ENCRYPTION_ENABLED
              value: 'no'
            - name: SPARK_SSL_ENABLED
              value: 'no'
            - name: SPARK_LOCAL_STORAGE_ENCRYPTION_ENABLED
              value: 'no'
            - name: SPARK_LOCAL_DIRS
              value: /tmp
```

This section defines:

Container Configuration:
- Name: `spark-master`
- Image: `custom-spark:latest`
- Image pull policy: `IfNotPresent` (uses local image if available)

Exposed Ports:
- 7077: Spark RPC port for internal communication
- 8080: Web UI port for monitoring and management

Environment Variables:
- `SPARK_MODE`: Set to "master" for master node configuration
- Security settings (all disabled for development):
  - RPC authentication
  - RPC encryption
  - SSL
  - Local storage encryption
- Local storage directory set to `/tmp`

### Service Metadata

```yaml
apiVersion: v1
kind: Service
metadata:
  name: spark-master-service
```

This section defines:
- API version: `v1` for Service resources
- Resource type: `Service`
- Service name: `spark-master-service`

### Service Specification

```yaml
spec:
  ports:
    - port: 7077
      name: rpc
    - port: 8080
      name: webui
  selector:
    app: spark-master
```

This section configures:
- Exposed ports:
  - 7077: RPC port for Spark communications
  - 8080: Web UI port for monitoring
- Pod selector to identify which pods to expose
- Makes the Spark master accessible within the cluster


