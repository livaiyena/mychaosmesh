#!/bin/bash

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
NAMESPACE="chaos-demo"
EXPERIMENTS_DIR="$SCRIPT_DIR/../chaos-experiments"
LOG_DIR="$SCRIPT_DIR/../logs"
SERVICE_URL="http://localhost:5000/api/data"

# Ensure log directory exists
mkdir -p "$LOG_DIR"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

run_experiment() {
    local exp_file=$1
    local exp_name=$(basename "$exp_file" .yaml)
    local log_file="$LOG_DIR/$exp_name.log"

    log "Starting experiment: $exp_name"
    echo "=== Experiment: $exp_name ===" > "$log_file"

    # Start background loop to test connectivity continuously
    log "Starting continuous tests (10 requests)..."
    echo -e "\n=== Test Results during Chaos ===" >> "$log_file"
    
    (
        start_time=$SECONDS
        for ((counter=1; counter<=6; counter++)); do
            echo "Request $counter (T+$(($SECONDS - $start_time))s):" >> "$log_file"
            curl -s -w "\nStatus: %{http_code} Time: %{time_total}s\n" "$SERVICE_URL" >> "$log_file" 2>&1
            echo "------------------" >> "$log_file"
            sleep 2
        done
    ) &
    TEST_PID=$!

    # Apply experiment
    log "Applying chaos: $exp_file"
    kubectl apply -f "$exp_file" >> "$log_file" 2>&1
    
    # Wait for tests to finish
    wait $TEST_PID
    
    # Cleanup
    log "Cleaning up experiment..."
    kubectl delete -f "$exp_file" >> "$log_file" 2>&1
    
    log "Experiment $exp_name completed. Logs: $log_file"
    echo -e "\n=== Experiment Completed ===" >> "$log_file"
}

# Main execution
log "Starting Chaos Mesh Experiments Suite"

# Check if cluster is reachable
if ! kubectl cluster-info > /dev/null 2>&1; then
    log "Error: Kubernetes cluster not reachable"
    exit 1
fi

# Setup Port Forwarding
log "Setting up port-forward to frontend-service..."
kubectl port-forward -n "$NAMESPACE" svc/frontend-service 5000:5000 > /dev/null 2>&1 &
PF_PID=$!

# Cleanup function
cleanup() {
    kill $PF_PID 2>/dev/null
}
trap cleanup EXIT

log "Waiting 5s for port-forward..."
sleep 5

# Run experiments sequentially
for exp in "$EXPERIMENTS_DIR"/*.yaml; do
    run_experiment "$exp"
    log "Waiting 5s before next experiment..."
    sleep 5
done

log "All experiments completed."