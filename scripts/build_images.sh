#!/bin/bash

# Build script for Project
# This script builds the docker images inside Minikubes Docker daemon.

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$SCRIPT_DIR/.."

echo "=== Building Docker Images for My Chaos Mesh Project ==="

# Check for minikube
if command -v minikube &> /dev/null; then
    echo "Configuring Docker environment for Minikube..."
    eval $(minikube -p minikube docker-env)
else
    echo "Minikube not found. Assuming local Docker environment."
fi

# Build Frontend
echo "Building Frontend..."
docker build -t mychaos-frontend:latest "$ROOT_DIR/app/frontend"

# Build Backend
echo "Building Backend..."
docker build -t mychaos-backend:latest "$ROOT_DIR/app/backend"

# Build DataService
echo "Building DataService..."
docker build -t mychaos-dataservice:latest "$ROOT_DIR/app/dataservice"

echo "=== Build Complete ==="
echo "Images built:"
docker images | grep mychaos
