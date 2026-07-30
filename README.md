# Flask App — Containerization & CI/CD Assessment

## Bug Fix Explanation

The app was binding to `host="127.0.0.1"` (localhost only), which prevents Docker from
forwarding traffic into the container since the process only listens on the loopback
interface. The fix was changing the host to `"0.0.0.0"` in `app.py` so the Flask server
accepts connections on all network interfaces, making it reachable via the mapped port.

---

## Links

- **GitHub Repository:** `https://github.com/KambleSahil3/PythonFlaskApp`
- **Docker Hub Image:** `https://hub.docker.com/r/kamble3sahil/flask-app`

---

## Local Setup & Execution Guide

### Prerequisites
- Docker & Docker Compose installed
- Python 3.11+ (for running tests locally)

### 1. Clone the repository
```bash
git clone https://github.com/KambleSahil3/PythonFlaskApp.git
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
docker pull kamble3sahil/flask-app:latest
docker run -p 5000:5000 kamble3sahil/flask-app:latest
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

kubectl apply -f k8s/

kubectl get pods          # wait for Running status
minikube service flask-app-service   # opens the app in browser
```

## Live Demo Video

[Watch the walkthrough here](<PASTE_VIDEO_LINK_HERE>)

---