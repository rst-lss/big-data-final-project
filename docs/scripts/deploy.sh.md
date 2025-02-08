# `deploy.sh`

This document explains the key commands in the `deploy.sh` script, which is used to automate the deployment process of the project. The script sets up Minikube, builds Docker images, and deploys various components to Kubernetes. While the script includes some helper functions, this document focuses only on the main deployment-related commands.

### Start Minikube

```bash
print_message "$YELLOW" "Starting Minikube..."
if ! minikube status | grep -q "Running"; then
    minikube start --feature-gates=PodIndexLabel=true --cpus="4" --memory="6g"
    check_status "Minikube started"
else
    print_message "$GREEN" "✓ Minikube is already running"
fi
```

- Checks if Minikube is already running; if not, starts Minikube with specific resource configurations.
- `--cpus="4" --memory="6g"` ensures Minikube has sufficient resources to run the deployments smoothly.
- `--feature-gates=PodIndexLabel=true` enables advanced pod indexing for Kubernetes.

### Build Docker Images

```bash
print_message "$YELLOW" "Switching to Minikube's Docker daemon..."
eval $(minikube docker-env)
check_status "Switched to Minikube's Docker daemon"
```

- Switches to Minikube’s internal Docker daemon to build images directly within the Minikube environment.

```bash
print_message "$YELLOW" "Building Data Ingestor Docker image..."
docker build -t data-ingestor:latest ./src/data-ingestor/
check_status "Docker images built"
```

- Builds a Docker image for the data ingestor component and tags it as `data-ingestor:latest`.
- Similar steps are followed for Spark (`custom-spark:latest`) and the ensemble model (`ensemble-model:latest`).

### Deploy Kafka Cluster

```bash
print_message "$YELLOW" "Applying Kubernetes configurations..."

kubectl apply -f src/kafka-cluster/zookeeper-deployment.yaml
kubectl wait --for=condition=Ready pod -l app=zookeeper
kubectl apply -f src/kafka-cluster/kafka-deployment.yaml
```

- Deploys Zookeeper and waits for it to be ready before proceeding.
- Deploys the Kafka cluster once Zookeeper is running.

### Deploy Data Ingestor

```bash
kubectl wait --for=condition=Ready pod/kafka-0
kubectl apply -f src/data-ingestor/data-ingestor-deployment.yaml
```

- Ensures Kafka is fully running before deploying the data ingestor component.

### Deploy Spark Cluster

```bash
kubectl apply -f src/spark-cluster/spark-master-deployment.yaml
kubectl wait --for=condition=Ready pod -l app=spark-master
kubectl apply -f src/spark-cluster/spark-worker-deployment.yaml
```

- Deploys Spark Master first and waits for it to be ready before deploying Spark Worker nodes.

### Deploy Ensemble Model

```bash
kubectl wait --for=condition=Ready pod -l app=spark-worker
kubectl apply -f src/ensemble-model/ensemble-model-deployment.yaml

kubectl wait --for=condition=Ready pod -l app=ensemble-model
check_status "Deployment configuration applied"
```

- Ensures Spark Workers are ready before deploying the ensemble model.
- Waits for the ensemble model deployment to be complete before confirming the deployment status.

### Check Pods and Services

```bash
print_message "$YELLOW" "Getting ingress IP..."
echo "Service URL:"
minikube ip

echo -e "\nPod Status:"
kubectl get pods
```

- Retrieves the Minikube IP to access services.
- Lists all running pods to verify the deployment status.



