# `zookeeper-deployment.yaml`

This file configures a Zookeeper instance inside Kubernetes using Bitnami's Zookeeper image. The deployment ensures a single Zookeeper instance is always available, supports health checks, and provides a stable service for Kafka brokers and other distributed systems. This setup is essential for managing distributed applications efficiently.

Zookeeper is a centralized service for maintaining configuration information, naming, and providing distributed synchronization. It is essential for managing Kafka brokers in a cluster.

## Deployment Configuration
### Deployment Definition

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: zookeeper
```

This section defines a Kubernetes `Deployment` named `zookeeper`. A Deployment ensures that the Zookeeper pod is always running and can be recreated if it fails.

### Deployment Specification

```yaml
spec:
  replicas: 1
  selector:
    matchLabels:
      app: zookeeper
  template:
    metadata:
      labels:
        app: zookeeper
```

- `replicas: 1` ensures that only a single instance of Zookeeper is running.
- `selector` and `labels` ensure that the Deployment manages only pods labeled `app: zookeeper`.

### Zookeeper Container Configuration

```yaml
  template:
    metadata:
      labels:
        app: zookeeper
    spec:
      containers:
        - name: zookeeper
          image: bitnami/zookeeper:latest
          imagePullPolicy: IfNotPresent
          ports:
            - containerPort: 2181
              name: client
```

- Uses the `bitnami/zookeeper:latest` image to deploy Zookeeper.
- Exposes port `2181` for client communication.
- `imagePullPolicy: IfNotPresent` ensures the image is pulled only if it is not already available locally.

### Health Checks (Readiness Probe)

```yaml
          readinessProbe:
            tcpSocket:
              port: 2181
            timeoutSeconds: 5
            periodSeconds: 10
            initialDelaySeconds: 15
```

- `readinessProbe`: Ensures the Zookeeper instance is ready before receiving traffic.
- Uses a TCP socket check on port `2181` to determine readiness.
- `initialDelaySeconds: 15` allows some time for Zookeeper to initialize before performing the first check.

### Environment Variables

```yaml
          env:
            - name: ALLOW_ANONYMOUS_LOGIN
              value: 'yes'
```

- `ALLOW_ANONYMOUS_LOGIN: 'yes'` allows clients to connect without authentication, which is useful for testing but should be secured in production.

## Zookeeper Service Configuration

### Service Definition

```yaml
apiVersion: v1
kind: Service
metadata:
  name: zookeeper
  labels:
    app: zookeeper
```

This section defines a Kubernetes `Service` named `zookeeper`, providing a stable way for clients to connect to the Zookeeper instance.

### Service Exposure

```yaml
spec:
  selector:
    app: zookeeper
  ports:
    - port: 2181
      name: client
```

- Maps port `2181` to allow client communication.
- The `selector` ensures that only the `zookeeper` pod is targeted by this service.


