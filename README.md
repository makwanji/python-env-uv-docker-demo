# Python Environments, uv & Docker Demo

A hands-on repository demonstrating Python environment management, multiple Python versions, modern dependency management with [`uv`](https://docs.astral.sh/uv/), and containerization using Docker, Docker Buildx Bake, and Docker Compose.

The repository includes two independent Python applications:

- **Hello API** — a REST API built with FastAPI.
- **Hello Web** — a web application built with Flask.

Both applications can run locally in isolated Python environments or as Docker containers.

## Learning Objectives

By working through this repository, you will learn how to:

- Create and manage Python virtual environments.
- Work with multiple Python versions, such as Python 3.11 and 3.12.
- Understand the differences between `venv`, `pip`, `uv`, `pyproject.toml`, `uv.lock`, and `requirements.txt`.
- Manage dependencies and lockfiles with `uv`.
- Build Python applications using FastAPI and Flask.
- Create efficient Docker images using `uv`.
- Use Docker Buildx Bake to build multiple images.
- Use Docker Compose to run multiple containers together.
- Apply basic container security practices, including non-root users, read-only filesystems, and health checks.

## Repository Structure

```text
python-env-uv-docker-demo/
├── README.md
├── .gitignore
├── .dockerignore
├── docker-bake.hcl
├── compose.yml
├── 01-venv/
│   └── README.md
├── 02-uv/
│   └── README.md
└── apps/
    ├── api/
    │   ├── pyproject.toml
    │   ├── uv.lock
    │   ├── requirements.txt
    │   ├── Dockerfile
    │   └── app/
    │       ├── __init__.py
    │       └── main.py
    └── web/
        ├── pyproject.toml
        ├── uv.lock
        ├── requirements.txt
        ├── Dockerfile
        └── app/
            ├── __init__.py
            └── main.py
```

## Prerequisites

Install the following tools on macOS, Linux, or a compatible development environment:

- Python
- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- Git
- Docker Desktop or Docker Engine with Docker Buildx and Docker Compose

Verify the installations:

```bash
python3 --version
uv --version
git --version
docker --version
docker buildx version
docker compose version
```

Ensure Docker is running before building or starting containers.

## 1. Python Virtual Environments

Python virtual environments isolate packages used by different projects.

This repository demonstrates separate environments using Python 3.11 and Python 3.12.

### Install Python versions

```bash
uv python install 3.11 3.12
uv python list
```

### Create environments

```bash
uv venv --python 3.11 01-venv/.venv311
uv venv --python 3.12 01-venv/.venv312
```

### Activate Python 3.11

```bash
source 01-venv/.venv311/bin/activate

python --version
which python

deactivate
```

### Activate Python 3.12

```bash
source 01-venv/.venv312/bin/activate

python --version
which python

deactivate
```

**Key takeaway:** a virtual environment isolates installed packages. The Python interpreter itself must also be available, which `uv` can manage.

## 2. Python Dependency Management with uv

[`uv`](https://docs.astral.sh/uv/) is a fast Python package and project manager. It supports interpreter management, virtual environments, dependency resolution, lockfiles, and running applications.

### Key files

| File | Purpose |
| --- | --- |
| `pyproject.toml` | Project metadata, Python requirements, direct dependencies, and tool configuration |
| `uv.lock` | Resolved dependency versions and lock information |
| `requirements.txt` | Package list in a format compatible with pip |
| `.python-version` | Specifies the project's preferred Python version |

### Common commands

```bash
# Install Python
uv python install 3.12

# Initialize a project
uv init --bare --python 3.12

# Add a dependency
uv add requests

# Update the lockfile
uv lock

# Synchronize the environment
uv sync --locked

# Run Python in the project environment
uv run python --version

# Run a script
uv run python app.py
```

### Export requirements.txt

The project uses `pyproject.toml` and `uv.lock` as its dependency-management source of truth.

Generate a pip-compatible requirements file with:

```bash
uv export \
  --locked \
  --no-dev \
  --format requirements-txt \
  --no-emit-project \
  -o requirements.txt
```

Run this command from the relevant application directory.

Regenerate the exported file whenever the project's dependencies change.

## 3. Hello API — FastAPI

The API application uses FastAPI and Uvicorn.

### Run locally

```bash
cd apps/api

uv sync --locked
uv run uvicorn app.main:app \
  --host 127.0.0.1 \
  --port 8000 \
  --reload
```

Available endpoints:

| Endpoint | Description |
| --- | --- |
| `/` | Hello World response with the Python version |
| `/health` | Health check |
| `/docs` | Interactive API documentation |

Open:

- <http://localhost:8000/>
- <http://localhost:8000/health>
- <http://localhost:8000/docs>

Stop the application with `Ctrl+C`.

## 4. Hello Web — Flask

The web application uses Flask. Its Docker configuration uses Gunicorn as the application server.

### Run locally

```bash
cd apps/web

uv sync --locked
uv run flask --app app.main run \
  --host 127.0.0.1 \
  --port 5000 \
  --debug
```

Available endpoints:

| Endpoint | Description |
| --- | --- |
| `/` | Hello World HTML page |
| `/health` | Health check |

Open:

- <http://localhost:5000/>
- <http://localhost:5000/health>

The Flask development server is intended for local development only. The container uses Gunicorn instead.

## 5. Docker Images

Each application has an independent Dockerfile.

The Dockerfiles use `uv` to install dependencies directly from `pyproject.toml` and `uv.lock`.

Example:

```dockerfile
COPY pyproject.toml uv.lock ./

RUN uv sync --locked --no-dev --no-install-project
```

### Why use uv in Docker?

- Fast dependency installation.
- Lockfile-based dependency resolution.
- Dependency installation can be cached separately from application source.
- No need to use pip to install application dependencies.
- The final image does not need to run `uv sync` at container startup.

The Dockerfiles also demonstrate basic container hardening:

- Non-root application users.
- Python output sent directly to container logs.
- Python bytecode generation configured for the image.
- Container health checks.
- Dependency installation before source-code copying for better build caching.

## 6. Build Both Images with Docker Buildx Bake

The root-level `docker-bake.hcl` defines the API and web image build targets.

Default tags:

- `hello-api:1.0`
- `hello-web:1.0`

### Preview the build configuration

```bash
docker buildx bake --print
```

### Build both images

```bash
docker buildx bake
```

### Build individual images

```bash
docker buildx bake api
docker buildx bake web
```

### Verify the images

```bash
docker images | grep hello-
```

Buildx Bake allows multiple image builds to be managed through one configuration rather than requiring separate manual build commands.

## 7. Run the Demo with Docker Compose

The root-level `compose.yml` defines both applications.

### Start the applications

From the repository root:

```bash
docker compose up -d
```

The Compose file references the locally built images, so build them first with `docker buildx bake`.

### Access the applications

| Application | URL |
| --- | --- |
| Hello API | <http://localhost:8000/> |
| API health | <http://localhost:8000/health> |
| API documentation | <http://localhost:8000/docs> |
| Hello Web | <http://localhost:5000/> |
| Web health | <http://localhost:5000/health> |

The demo binds its published ports to `127.0.0.1`, so the applications are accessible from the host machine without exposing those ports on all network interfaces.

### Verify the containers

```bash
docker compose ps
docker compose logs -f
```

### Test the endpoints

```bash
curl http://localhost:8000/
curl http://localhost:8000/health

curl http://localhost:5000/
curl http://localhost:5000/health
```

### Stop the demo

```bash
docker compose down
```

## 8. Development Workflow

When changing application dependencies, update the project configuration and lockfile, then regenerate `requirements.txt`.

For example, in the API project:

```bash
cd apps/api

uv add httpx
uv lock

uv export \
  --locked \
  --no-dev \
  --format requirements-txt \
  --no-emit-project \
  -o requirements.txt
```

Return to the repository root and rebuild the images:

```bash
cd ../..

docker buildx bake
docker compose up -d
```

Because Docker installs dependencies in a separate layer, changing only application source code can reuse the cached dependency layer.

**Important:** keep `pyproject.toml` and `uv.lock` committed. Treat `requirements.txt` as a generated export rather than an independently maintained dependency list.

## 9. Container Security Practices

This repository demonstrates a starting point for secure container builds.

- **Non-root execution:** the applications run as an unprivileged user.
- **Read-only filesystem:** Compose configures the containers with a read-only root filesystem and a writable `/tmp`.
- **Reduced privileges:** unnecessary Linux capabilities are dropped.
- **Health checks:** each image defines a health check endpoint.
- **Minimal base images:** the applications use Python slim images.
- **Dependency locking:** the build uses `uv sync --locked`.
- **Local-only ports:** published ports bind to the loopback interface.

For production use, consider additionally:

- Pinning base images by immutable digest.
- Scanning dependencies and container images for vulnerabilities.
- Adding automated unit and integration tests.
- Generating a software bill of materials (SBOM).
- Signing images and verifying provenance.
- Publishing images to a private or trusted container registry.
- Using GitHub Actions to build and scan images on pull requests.
- Managing secrets through a secret manager instead of baking them into images.
- Setting CPU and memory limits appropriate to the workload.

## 10. Future Enhancements

Planned extensions for this learning repository:

- [ ] Add GitHub Actions CI workflows.
- [ ] Add automated tests for API and web endpoints.
- [ ] Add Ruff linting and formatting.
- [ ] Add Trivy vulnerability scanning.
- [ ] Compare pip-based Docker builds with uv-based builds.
- [ ] Add multi-stage Docker builds and image-size comparisons.
- [ ] Add GHCR publishing.
- [ ] Add SBOM generation and image signing.
- [ ] Add Docker Compose integration tests.
- [ ] Add a small Kubernetes deployment example.

## Summary

This repository provides a practical progression from Python fundamentals to containerized applications:

1. Understand Python versions and virtual environments.
2. Manage dependencies with `uv`.
3. Understand `pyproject.toml`, `uv.lock`, and `requirements.txt`.
4. Develop a FastAPI API and Flask web application.
5. Build reproducible Docker images.
6. Orchestrate multi-image builds with Docker Buildx Bake.
7. Run the complete demo with Docker Compose.
8. Extend the project with DevSecOps automation and container security.

The goal is to create a reproducible, easy-to-understand reference project that can be extended into a production-oriented Python and DevSecOps workflow.
