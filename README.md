# My Chaos Mesh Project

A Chaos Engineering workshop project demonstrating simplified microservices and chaos experiments on Kubernetes.

## Architecture

Frontend (5000) -> Backend (5001) -> DataService (5002)

## Chaos Experiments

1. **Network Packet Loss**: 80% packet loss between Frontend and Backend.
2. **Network Delay**: 5 seconds delay to DataService.
3. **DataService Failure**: Pod kill experiment on DataService.
4. **Workflow Stress**: Combined CPU stress and network delay.

## How to Run

1. **Prerequisites**:
    - Kubernetes Cluster (Minikube/Kind)
    - Chaos Mesh installed
    - `kubectl` configured

2.  **Build Images**:
    ```bash
    cd mychaosmesh/scripts
    chmod +x build_images.sh
    ./build_images.sh
    ```

3.  **Deploy Application**:
    ```bash
    kubectl apply -f mychaosmesh/k8s/
    ```

4.  **Run Experiments**:
    ```bash
    cd mychaosmesh/scripts
    chmod +x run_experiments.sh
    ./run_experiments.sh
    ```

    This script will:
    - Apply each experiment.
    - Run curl tests against the frontend.
    - Log results to `mychaosmesh/logs/`.
    - Clean up after each experiment.

## Logs

Logs are stored in `mychaosmesh/logs/` with detailed timestamps and curl outputs.
