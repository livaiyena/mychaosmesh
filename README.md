# My Chaos Mesh Project

A Chaos Engineering demo project for testing microservice resilience on Kubernetes.

## Table of Contents

- [About](#about)
- [Architecture](#architecture)
- [Technologies](#technologies)
- [Setup](#setup)
- [Chaos Experiments](#chaos-experiments)
- [Project Structure](#project-structure)

---

## About

This project demonstrates Chaos Engineering principles using Chaos Mesh on Kubernetes. It includes three Python Flask microservices that are subjected to various failure scenarios to observe system behavior under stress.

### Goals
- Observe system behavior during unexpected failures
- Simulate network delays, packet loss, and resource exhaustion
- Learn Chaos Mesh tooling through hands-on experiments

---

## Architecture

```
+-------------+      +-------------+      +---------------+
|  Frontend   |----->|   Backend   |----->|  DataService  |
| (Port 5000) |      | (Port 5001) |      |  (Port 5002)  |
+-------------+      +-------------+      +---------------+
      |                    |                     |
      +--------------------+---------------------+
                    Kubernetes Cluster
                    (chaos-demo namespace)
```

**Services:**
- **Frontend**: Entry point for user requests
- **Backend**: Business logic layer
- **DataService**: Data processing simulation

---

## Technologies

| Category | Technology |
|----------|-----------|
| Application | Python 3.11, Flask |
| Container | Docker |
| Orchestration | Kubernetes (Minikube) |
| Chaos Engineering | Chaos Mesh |
| Automation | Bash, Python |

---

## Setup

### Prerequisites
- Docker
- Minikube or Kubernetes cluster
- kubectl
- Helm 3.x
- Chaos Mesh installed

### 1. Start Minikube
```bash
minikube start --driver=docker
```

### 2. Install Chaos Mesh
```bash
helm repo add chaos-mesh https://charts.chaos-mesh.org
kubectl create ns chaos-mesh
helm install chaos-mesh chaos-mesh/chaos-mesh -n chaos-mesh \
  --set chaosDaemon.runtime=containerd \
  --set chaosDaemon.socketPath=/run/containerd/containerd.sock
```

### 3. Build Docker Images
```bash
cd scripts
chmod +x build_images.sh
./build_images.sh
```

### 4. Deploy Application
```bash
kubectl apply -f k8s/
```

### 5. Wait for Pods
```bash
kubectl get pods -n chaos-demo -w
```

---

## Chaos Experiments

| # | Experiment | Description | Expected Effect |
|---|------------|-------------|-----------------|
| 01 | Network Packet Loss | 50% packet loss Frontend to Backend | Timeouts, 503 errors |
| 02 | Network Delay | 1s delay Backend to DataService | High latency, timeouts |
| 03 | DataService Failure | 100% packet loss to DataService | Service unreachable |
| 04 | Workflow Stress | CPU stress + Network delay combined | Performance degradation |
| 05 | Backend CPU Stress | High CPU usage on Backend | Slow response times |
| 06 | High Jitter Mixed | Random delays (4s jitter) | Mixed success/failure |

### Running Experiments
```bash
cd scripts
chmod +x run_experiments.sh
./run_experiments.sh
```

The script will:
- Apply each experiment sequentially
- Send test requests
- Log results to `logs/`
- Clean up after each experiment

---

## Project Structure

```
mychaosmesh/
├── app/                          # Microservices
│   ├── frontend/
│   ├── backend/
│   └── dataservice/
├── k8s/                          # Kubernetes manifests
├── chaos-experiments/            # Chaos Mesh experiments
├── scripts/                      # Automation scripts
└── logs/                         # Experiment outputs
```

---

## License

This project is for educational purposes.
