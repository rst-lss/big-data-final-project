# `kafka-deployment.yaml`

This file configures a Kafka cluster inside Kubernetes using Bitnami's Kafka image. It defines a StatefulSet for broker persistence, a headless service for inter-broker communication, and persistent storage for data durability. With this setup, the Kafka cluster is highly available, scalable, and resilient to failures.

### Deployment Definition

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: kafka
```

This section defines a Kubernetes `StatefulSet` named `kafka`. A StatefulSet ensures each Kafka broker has a stable identity and persistent storage across restarts.

### StatefulSet Specification

```yaml
spec:
  serviceName: kafka-headless
  replicas: 2
  selector:
    matchLabels:
      app: kafka
  template:
    metadata:
      labels:
        app: kafka
```

- `serviceName: kafka-headless` associates this StatefulSet with a headless service for inter-broker communication.
- `replicas: 2` defines two Kafka broker instances for redundancy.
- `matchLabels` and `template.metadata.labels` ensure that only pods labeled `app: kafka` belong to this StatefulSet.

### Kafka Container Configuration

```yaml
  template:
    metadata:
      labels:
        app: kafka
    spec:
      containers:
        - name: kafka
          image: bitnami/kafka:latest
          imagePullPolicy: IfNotPresent
          ports:
            - containerPort: 9092
              name: kafka
            - containerPort: 9093
              name: kafka-internal
```

- Defines the Kafka container using `bitnami/kafka:latest`.
- Exposes two ports:
  - `9092`: External client communication.
  - `9093`: Internal inter-broker communication.

#### Health Checks (Readiness and Liveness Probes)

```yaml
          readinessProbe:
            tcpSocket:
              port: 9092
            timeoutSeconds: 5
            periodSeconds: 5
            initialDelaySeconds: 20
          livenessProbe:
            exec:
              command:
                - sh
                - -c
                - kafka-broker-api-versions.sh --bootstrap-server=localhost:9093
            timeoutSeconds: 5
            periodSeconds: 5
            initialDelaySeconds: 20
```

- `readinessProbe`: Ensures the broker is ready to accept traffic.
- `livenessProbe`: Ensures the broker remains operational by running a Kafka API check.

#### Kafka Configuration Environment Variables

```yaml
          env:
            - name: KAFKA_BROKER_ID
              valueFrom:
                fieldRef:
                  fieldPath: metadata.labels['apps.kubernetes.io/pod-index']
            - name: POD_NAME
              valueFrom:
                fieldRef:
                  fieldPath: metadata.name
            - name: POD_NAMESPACE
              valueFrom:
                fieldRef:
                  fieldPath: metadata.namespace
            - name: KAFKA_CFG_ZOOKEEPER_CONNECT
              value: zookeeper:2181
            - name: KAFKA_CFG_LISTENER_SECURITY_PROTOCOL_MAP
              value: INTERNAL:PLAINTEXT,EXTERNAL:PLAINTEXT
            - name: KAFKA_CFG_LISTENERS
              value: INTERNAL://:9093,EXTERNAL://:9092
            - name: KAFKA_CFG_ADVERTISED_LISTENERS
              value: INTERNAL://$(POD_NAME).kafka-headless.$(POD_NAMESPACE).svc.cluster.local:9093,EXTERNAL://$(POD_NAME).kafka-headless.$(POD_NAMESPACE).svc.cluster.local:9092
            - name: KAFKA_INTER_BROKER_LISTENER_NAME
              value: INTERNAL
            - name: ALLOW_PLAINTEXT_LISTENER
              value: 'yes'
```

- Sets essential environment variables:
  - `KAFKA_BROKER_ID`: Assigns a unique ID to each broker.
  - `KAFKA_CFG_ZOOKEEPER_CONNECT`: Connects Kafka to Zookeeper.
  - `KAFKA_CFG_LISTENERS`: Defines internal and external listener ports.
  - `KAFKA_CFG_ADVERTISED_LISTENERS`: Advertises Kafka broker addresses.
  - `ALLOW_PLAINTEXT_LISTENER`: Enables plaintext communication.

#### Storage Configuration

```yaml
          volumeMounts:
            - name: kafka-data
              mountPath: /bitnami/kafka
```

- Mounts a persistent volume named `kafka-data` at `/bitnami/kafka` to ensure data persistence across pod restarts.

### Persistent Volume Configuration

```yaml
  volumeClaimTemplates:
    - metadata:
        name: kafka-data
      spec:
        accessModes: [ReadWriteOnce]
        resources:
          requests:
            storage: 10Gi
```

- `volumeClaimTemplates` ensures each Kafka broker gets a dedicated persistent volume.
- `storage: 10Gi` reserves 10 GB for Kafka data.
- `ReadWriteOnce` allows read/write access by a single pod at a time.

### Kafka Service Configuration

```yaml
apiVersion: v1
kind: Service
metadata:
  name: kafka-headless
  labels:
    app: kafka
```

This section defines a Kubernetes `Service` named `kafka-headless`, which allows stable DNS resolution for Kafka brokers in the cluster.

### Service Exposure

```yaml
spec:
  ports:
    - port: 9092
      name: kafka
    - port: 9093
      name: kafka-internal
  clusterIP: None
  selector:
    app: kafka
```

- Defines the ports `9092` and `9093` for external and internal access.
- `clusterIP: None` makes it a headless service, allowing direct communication between Kafka brokers.
- The `selector` ensures that only Kafka pods are associated with this service.