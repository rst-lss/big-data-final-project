# `Dockerfile`

This document provides a detailed explanation of the Dockerfile used to create a base image for all Spark machines. Since we want to ensure that all dependencies are satisfied in each machine, we create a custom Docker image based on `bitnami/spark` and install the necessary dependencies. This image is then used as the container for all Spark instances.


## Dockerfile Configuration

### Base Image

```dockerfile
FROM bitnami/spark:latest
```

- `FROM bitnami/spark:latest` sets the base image as `bitnami/spark`, ensuring that all necessary Spark configurations and binaries are pre-installed.
- This base image is maintained by Bitnami and provides an optimized Spark runtime.
- Using `latest` ensures that the most recent stable version of the image is used, though specifying a fixed version can improve reproducibility.

### Setting Up the Application Environment

```dockerfile
WORKDIR /app
```

- `WORKDIR /app` sets `/app` as the working directory inside the container.
- This ensures that all subsequent commands (such as copying files or running applications) operate within this directory.

### Installing Dependencies

```dockerfile
COPY requirements.txt /app/
RUN pip install -r requirements.txt
```

- `COPY requirements.txt /app/` copies the `requirements.txt` file from the local machine to the `/app/` directory in the container.
- `RUN pip install -r requirements.txt` installs the Python dependencies listed in `requirements.txt`.
- This step ensures that all required Python packages are available within the container for Spark applications that depend on them.




