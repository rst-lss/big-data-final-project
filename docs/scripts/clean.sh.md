# `clean.sh`

This document explains the `clean.sh` script, which is used to undo all the deployments performed by `deploy.sh`. It removes all deployed Kubernetes components and optionally stops and deletes the Minikube instance.

### Remove Pods and Services

```bash
kubectl delete -f src/kafka-cluster/zookeeper-deployment.yaml
kubectl delete -f src/kafka-cluster/kafka-deployment.yaml
kubectl delete -f src/spark-cluster/spark-master-deployment.yaml
kubectl delete -f src/spark-cluster/spark-worker-deployment.yaml
kubectl delete -f src/data-ingestor/data-ingestor-deployment.yaml
kubectl delete -f src/ensemble-model/ensemble-model-deployment.yaml
```

- Deletes all Kubernetes deployments related to Kafka, Zookeeper, Spark Master, Spark Workers, Data Ingestor, and the Ensemble Model.
- Ensures that no resources remain active after cleanup.

### Quit Minikube

```bash
read -p "Do you want to STOP Minikube container? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    minikube stop

    read -p "Do you want to also **DELETE** Minikube container? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        minikube delete
    fi
fi
```

- Prompts the user to confirm whether they want to stop Minikube.
- If confirmed, it stops Minikube to free up system resources.
- Further prompts the user to confirm whether they want to delete Minikube entirely.
- If confirmed, deletes Minikube, removing all associated data and configurations.


