### Big Data Final Project

In this project, we replicated Chapter 7 of the book *MACHINE LEARNING FOR DATA STREAMS with Practical Examples in MOA*, which discusses the use of ensemble methods on streaming data.

We used Spark and Kafka inside Kubernetes to simulate real-world data stream processing. Kafka was employed as the message broker and streaming cluster, while Spark acted as the executor node for our ensemble model.

#### Technologies Used:
- **Kafka**: Kafka is a distributed event streaming platform used for high-performance data pipelines, streaming analytics, and event-driven applications. It helps ensure reliable message passing between producers (data-ingestor) and consumers (ensemble model).
- **Spark**: Apache Spark is a distributed processing framework designed for big data workloads. It provides a fast, in-memory computing engine to run machine learning algorithms on streaming data.
- **Kubernetes**: Kubernetes is an orchestration system for managing containerized applications. It facilitates the deployment, scaling, and management of our Kafka and Spark clusters.

#### Data Stream
We used a Python script to read data from the **Adult Dataset** and send each row as a message into the Kafka broker.

**Adult Dataset**: The Adult dataset is a widely used dataset from the UCI Machine Learning Repository. It contains demographic information and income-related attributes, typically used for classification tasks to predict whether an individual's income exceeds $50K per year.

### Table of Contents
- **Scripts**
  - [`deploy.sh.md`](./scripts/deploy.sh.md)
  - [`clean.sh.md`](./scripts/clean.sh.md)
- **Data Ingestor**
  - [`Dockerfile.md`](./data-ingestor/Dockerfile.md)
  - [`data-ingestor-deployment.yaml.md`](./data-ingestor/data-ingestor-deployment.yaml.md)
  - [`data-ingestor.py.md`](./data-ingestor/data-ingestor.py.md)
- **Ensemble Model**
  - [`Dockerfile.md`](./ensemble-model/Dockerfile.md)
  - [`ensemble-model.py.md`](./ensemble-model/ensemble-model.py.md)
  - [`ensemble-model-deployment.yaml.md`](./ensemble-model/ensemble-model-deployment.yaml.md)
  - [`spark-submit-ensemble-model.sh.md`](./ensemble-model/spark-submit-ensemble-model.sh.md)
- **Kafka Cluster**
  - [`kafka-deployment.yaml.md`](./kafka-cluster/kafka-deployment.yaml.md)
  - [`zookeeper-deployment.yaml.md`](./kafka-cluster/zookeeper-deployment.yaml.md)
- **Spark Cluster**
  - [`Dockerfile.md`](./spark-cluster/Dockerfile.md)
  - [`spark-worker-deployment.yaml.md`](./spark-cluster/spark-worker-deployment.yaml.md)
  - [`spark-master-deployment.yaml.md`](./spark-cluster/spark-master-deployment.yaml.md)

This document provides an overview of our implementation. For detailed deployment configurations, refer to the respective configuration files.

