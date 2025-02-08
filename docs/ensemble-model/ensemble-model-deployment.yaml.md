# `ensemble-model-deployment.yaml`

This document describes the Kubernetes deployment and service configuration for the Spark driver that manages the PySpark job (`ensemble-model.py`). The configuration deploys a single replica of the ensemble model using a Docker container and exposes necessary ports through a Kubernetes service.

## Usage

To deploy this configuration:

1. Ensure your Kubernetes cluster is running and configured
2. Make sure the Docker image `ensemble-model:latest` is available
3. Apply the configuration using:
   ```bash
   kubectl apply -f ensemble-model-deployment.yaml
   ```
4. Verify the deployment:
   ```bash
   kubectl get deployments
   kubectl get pods
   kubectl get services
   ```

The deployment will create a single pod running the ensemble model, and the service will make it accessible within the cluster.


## Deployment Configuration

### Metadata and Labels

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ensemble-model
  labels:
    app: ensemble-model
```

This section defines:
- The API version (`apps/v1`) used for the Deployment resource
- The resource type as a `Deployment`
- A unique name for the deployment: `ensemble-model`
- Labels for identifying and selecting the deployment

### Replica and Selector Configuration

```yaml
  replicas: 1
  selector:
    matchLabels:
      app: ensemble-model
  template:
    metadata:
      labels:
        app: ensemble-model
```

This section specifies:
- The number of replica pods to maintain (`replicas: 1`)
- Label selectors to match pods with the deployment
- Pod template metadata with matching labels
- Ensures Kubernetes maintains exactly one running instance of the application

### Container Specification

```yaml
    spec:
      containers:
        - name: ensemble-model
          image: ensemble-model:latest
          imagePullPolicy: IfNotPresent
          ports:
            - containerPort: 7072
              name: headless-svc
            - containerPort: 8082
              name: web-ui
            - containerPort: 35635
              name: block-manager
          env:
            - name: SPARK_MASTER_URL
              value: spark://spark-master-service:7077
```

This section defines the container configuration:
- Container name: `ensemble-model`
- Docker image: `ensemble-model:latest`
- Image pull policy: `IfNotPresent` (uses local image if available)
- Exposed ports:
  - 7072: Headless service port
  - 8082: Spark Web UI port
  - 35635: Spark block manager port
- Environment variables:
  - Sets the Spark master URL to connect to the Spark cluster

## Service Configuration

### Service Metadata

```yaml
apiVersion: v1
kind: Service
metadata:
  name: ensemble-model-service
  labels:
    app: ensemble-model
```

This section defines:
- The API version (`v1`) for the Service resource
- The resource type as a `Service`
- A unique name for the service: `ensemble-model-service`
- Labels matching the deployment

### Service Specification

```yaml
spec:
  selector:
    app: ensemble-model
  ports:
    - port: 7072
      name: headless-svc
    - port: 8082
      name: web-ui
    - port: 35635
      name: block-manager
```

This section configures:
- Pod selector to identify which pods to expose
- Port mappings for the service:
  - 7072: Headless service port
  - 8082: Web UI access
  - 35635: Block manager communication
- Each port is named for easy reference in other resources