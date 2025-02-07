# Big Data Final Project

This repository contains the **Big Data** project by **Amin Haeri** and **Alireza Nazari**. The project is designed to handle real-time stream processing using distributed systems techniques and spark techonologies.

## Project Overview

The project implements Ensemble Learning on Stream Data. It leverages modern distributed systems tools and methodologies to achieve scalability and performance.

## Prerequisites

Before running the project, ensure the following tools are installed:

- **Minikube**
- **Kubectl**
- **Docker**

## Setup and Deployment

### Deploying the Project
To deploy the project, run the script located at:
```
/scripts/deploy.md
```

### Cleaning Up
To clean up the deployment, use the following script:
```
/scripts/clean.md
```

### Optimizing Minikube Startup
To speed up the Minikube startup process, cache the following Docker images:

- `bitnami/kafka`
- `bitnami/spark:latest`
- `bitnami/zookeeper`
- `python:3.9-slim`

Use the command below to add images to the Minikube cache:
```
minikube cache add <image>
```

## Getting Started

1. Install all prerequisites listed above.
2. Optimize Minikube with the caching instructions.
3. Obtain your API key from Alpha Vantage and configure the `.env` file.
4. Deploy the project using the provided deployment script.
5. Access the system and analyze the results.

