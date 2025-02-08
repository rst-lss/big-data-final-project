#!/bin/bash
echo "Cleaning up deployment..."

kubectl delete -f src/kafka-cluster/zookeeper-deployment.yaml
kubectl delete -f src/kafka-cluster/kafka-deployment.yaml
kubectl delete -f src/spark-cluster/spark-master-deployment.yaml
kubectl delete -f src/spark-cluster/spark-worker-deployment.yaml
kubectl delete -f src/data-ingestor/data-ingestor-deployment.yaml
kubectl delete -f src/ensemble-model/ensemble-model-deployment.yaml

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

echo "Cleanup completed!"
