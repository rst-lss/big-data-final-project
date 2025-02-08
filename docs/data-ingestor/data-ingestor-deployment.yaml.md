# `data-ingestor-deployment.yaml`

This Kubernetes deployment configuration file is used to deploy the `data-ingestor` script as a containerized application in a Kubernetes cluster. The deployment ensures that one replica of the `data-ingestor` Docker image is running, and it configures the necessary environment variables for the script to communicate with a Kafka broker.

### Describe Deployment Name

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: data-ingestor
```

**Explanation:**
- `apiVersion: apps/v1`: Specifies the API version for the Kubernetes Deployment object.
- `kind: Deployment`: Indicates that this is a Kubernetes Deployment, which is used to manage a replicated set of pods.
- `metadata.name: data-ingestor`: The name of the deployment, which will be used to identify it within the Kubernetes cluster.

### Describe State and Tags

```yaml
spec:
  replicas: 1
  selector:
    matchLabels:
      app: data-ingestor
```

**Explanation:**
- `spec.replicas: 1`: Specifies that only one replica (instance) of the `data-ingestor` pod should be running. This is a single-instance deployment.
- `spec.selector.matchLabels.app: data-ingestor`: Defines the label selector for the deployment. The deployment will manage pods that have the label `app: data-ingestor`.

### Describe Docker Container

```yaml
  template:
    metadata:
      labels:
        app: data-ingestor
    spec:
      containers:
        - name: data-ingestor
          image: data-ingestor:latest
          imagePullPolicy: IfNotPresent
          env:
            - name: KAFKA_BROKER
              value: kafka-0.kafka-headless:9092
            - name: KAFKA_TOPIC
              value: adult-stream
            - name: SEND_INTERVAL
              value: "0.5"
```

**Explanation:**
- `template.metadata.labels.app: data-ingestor`: Specifies the labels for the pods created by this deployment. The label `app: data-ingestor` matches the selector defined earlier.
- `template.spec.containers`: Defines the container(s) that will run within the pod.
  - `name: data-ingestor`: The name of the container.
  - `image: data-ingestor:latest`: The Docker image to use for the container. In this case, it uses the `data-ingestor:latest` image.
  - `imagePullPolicy: IfNotPresent`: Specifies that the image should only be pulled if it is not already present on the node. This can help reduce unnecessary image pulls.
  - `env`: Defines environment variables that will be passed to the container.
    - `KAFKA_BROKER`: The address of the Kafka broker. In this case, it is set to `kafka-0.kafka-headless:9092`.
    - `KAFKA_TOPIC`: The Kafka topic where the data will be sent. It is set to `adult-stream`.
    - `SEND_INTERVAL`: The time interval (in seconds) between sending each row of data to Kafka. It is set to `0.5` seconds.
