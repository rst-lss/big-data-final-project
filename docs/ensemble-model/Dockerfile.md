# `Dockerfile`

This Dockerfile is used to create a Docker image for an ensemble model implemented in PySpark. The image is designed to run the ensemble model in a containerized environment, which can then be deployed inside a Kubernetes cluster.

### Base Image

```dockerfile
FROM custom-spark:latest
```

**Explanation:**
- `FROM custom-spark:latest`: Specifies the base image for the Docker container. In this case, it uses a custom Spark image (`custom-spark:latest`). This image likely includes Apache Spark and any necessary dependencies pre-installed, making it suitable for running PySpark applications.


### Entry Point

```dockerfile
WORKDIR /app

COPY ensemble-model.py /app/
COPY --chmod=555 spark-submit-ensemble-model.sh /app/

CMD [ "/app/spark-submit-ensemble-model.sh" ]
```

**Explanation:**
- `WORKDIR /app`: Sets the working directory inside the container to `/app`. All subsequent commands will be run from this directory.
- `COPY ensemble-model.py /app/`: Copies the `ensemble-model.py` script from the host machine to the `/app` directory inside the container. This script contains the PySpark code for the ensemble model.
- `COPY --chmod=555 spark-submit-ensemble-model.sh /app/`: Copies the `spark-submit-ensemble-model.sh` script from the host machine to the `/app` directory inside the container. The `--chmod=555` option sets the script's permissions to `555`, making it executable (read and execute permissions for everyone).
- `CMD [ "/app/spark-submit-ensemble-model.sh" ]`: Specifies the command to run when the container starts. In this case, it runs the `spark-submit-ensemble-model.sh` script. The `CMD` instruction is used to define the default command for the container. This script likely contains the necessary `spark-submit` command to run the `ensemble-model.py` script with the appropriate Spark configuration.
