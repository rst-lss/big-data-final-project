# `Dockerfile.md`

This Dockerfile is used to create a Docker image for the `data-ingestor` script. The image is designed to run the Python script in a containerized environment, which can then be deployed inside a Kubernetes cluster.

### Base Image

```dockerfile
FROM python:3.9-slim
```

**Explanation:**
- `FROM python:3.9-slim`: Specifies the base image for the Docker container. In this case, it uses the official Python 3.9 slim image, which is a lightweight version of the Python image. This is ideal for reducing the size of the final Docker image while still providing the necessary Python runtime.


### Install Requirements

```dockerfile
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
```

**Explanation:**
- `WORKDIR /app`: Sets the working directory inside the container to `/app`. All subsequent commands will be run from this directory.
- `COPY requirements.txt .`: Copies the `requirements.txt` file from the host machine to the current working directory (`/app`) inside the container. This file typically lists the Python dependencies required by the script.
- `RUN pip install --no-cache-dir -r requirements.txt`: Installs the Python dependencies listed in `requirements.txt`. The `--no-cache-dir` option is used to avoid caching the downloaded packages, which helps reduce the size of the final Docker image.

### Entry Point

```dockerfile
COPY data-ingestor.py .

CMD ["python", "/app/data-ingestor.py"]
```

**Explanation:**
- `COPY data-ingestor.py .`: Copies the `data-ingestor.py` script from the host machine to the current working directory (`/app`) inside the container.
- `CMD ["python", "/app/data-ingestor.py"]`: Specifies the command to run when the container starts. In this case, it runs the `data-ingestor.py` script using the Python interpreter. The `CMD` instruction is used to define the default command for the container.


