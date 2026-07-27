# Flask App — Containerization & CI/CD Assessment

## Bug Fix Explanation

The app was binding to `host="127.0.0.1"` (localhost only), which prevents Docker from
forwarding traffic into the container since the process only listens on the loopback
interface. The fix was changing the host to `"0.0.0.0"` in `app.py` so the Flask server
accepts connections on all network interfaces, making it reachable via the mapped port.

---

## Links

- **GitHub Repository:** `https://github.com/<YOUR_GITHUB_USERNAME>/PythonFlaskApp`
- **Docker Hub Image:** `https://hub.docker.com/r/<YOUR_DOCKER_USERNAME>/flask-app`

---

## Local Setup & Execution Guide

### Prerequisites
- Docker & Docker Compose installed
- Python 3.11+ (for running tests locally)

### 1. Clone the repository
```bash
git clone https://github.com/<YOUR_GITHUB_USERNAME>/PythonFlaskApp.git
cd PythonFlaskApp
```

### 2. Configure environment variables
```bash
cp .env.example .env
# Edit .env if needed — defaults work for local development
```

### 3. Run with Docker Compose
```bash
docker compose up --build
```
App is available at `http://localhost:5000`

### 4. Test the endpoints
```bash
curl http://localhost:5000/
curl http://localhost:5000/health
```

### 5. Run unit tests
```bash
pip install -r requirements.txt
pytest test_app.py -v
# Expected: 2 passed (test_index, test_health)
```

### 6. Pull and run directly from Docker Hub
```bash
docker pull <YOUR_DOCKER_USERNAME>/flask-app:latest
docker run -p 5000:5000 <YOUR_DOCKER_USERNAME>/flask-app:latest
```

### 7. Run the health monitoring script
```bash
# While the app is running in another terminal:
./health_check.sh
```

---

## Kubernetes Local Deployment (Minikube)

### Prerequisites
- [Minikube](https://minikube.sigs.k8s.io/docs/start/) installed

```bash
minikube start

# Replace <DOCKER_USERNAME> in k8s/deployment.yaml with your Docker Hub username, then:
kubectl apply -f k8s/

kubectl get pods          # wait for Running status
minikube service flask-app-service   # opens the app in browser
```

---

## Architecture & Design Choices

### Dockerfile
Uses `python:3.11-slim` to keep the image small. Dependencies are installed before
copying source code to leverage Docker layer caching — rebuilds are fast when only
`app.py` changes.

### Docker Compose
Single-service compose file with `env_file: .env` for secrets injection and a native
`healthcheck` that polls `/health` every 10 seconds. No secrets are hardcoded.

### Secrets Management
- `.env` holds real values and is listed in `.gitignore` — never committed
- `.env.example` with placeholder values is committed as a template
- CI/CD uses GitHub Secrets (`DOCKER_USERNAME`, `DOCKER_PASSWORD`) for Docker Hub auth

### CI/CD Pipeline (GitHub Actions)
Three sequential jobs on every push/PR to `main`:
1. **test** — installs deps and runs `pytest`
2. **security-scan** — Trivy filesystem scan for CRITICAL/HIGH CVEs (`exit-code: 0` so it reports but doesn't block)
3. **build-and-push** — builds and pushes image to Docker Hub (push to `main` only), tagged as `latest` and `<git-sha>`

### Kubernetes
Standard `Deployment` (2 replicas) + `NodePort` Service. Liveness and readiness probes
both hit `/health` so Kubernetes automatically restarts unhealthy pods and only routes
traffic to ready ones.

---

## Live Demo Video

[Watch the walkthrough here](<PASTE_VIDEO_LINK_HERE>)

---

## Project Structure

```
PythonFlaskApp/
├── app.py                        # Flask application (bug fixed: host=0.0.0.0)
├── test_app.py                   # pytest test suite (2 tests)
├── requirements.txt              # Python dependencies
├── Dockerfile                    # Container build file (python:3.11-slim)
├── docker-compose.yml            # Local orchestration + health check
├── health_check.sh               # Health polling script (every 10s)
├── .env                          # Local secrets (gitignored)
├── .env.example                  # Secrets template (committed)
├── .gitignore
├── k8s/
│   ├── deployment.yaml           # Kubernetes Deployment (2 replicas + probes)
│   └── service.yaml              # Kubernetes Service (NodePort 30080)
├── .github/
│   └── workflows/
│       └── ci.yml                # GitHub Actions CI/CD pipeline
├── TASKSHEET.md                  # Assessment task checklist
└── VIDEO_SCRIPT.md               # Timestamped video walkthrough script
```
