#!/bin/bash
# NeuroForge 3D - Docker Build Validation Script
# This script validates that the Docker environment is correctly configured

set -e

echo "==================================="
echo "NeuroForge 3D - Build Validation"
echo "==================================="
echo ""

# Check if Docker is installed
echo "1. Checking Docker installation..."
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi
echo "✅ Docker found: $(docker --version)"
echo ""

# Check if nvidia-docker is available
echo "2. Checking NVIDIA Docker support..."
if ! docker run --rm --gpus all nvidia/cuda:12.1.0-base-ubuntu22.04 nvidia-smi &> /dev/null; then
    echo "⚠️  WARNING: NVIDIA GPU support not available or not configured."
    echo "   The container will build but GPU features won't work."
    echo "   Make sure nvidia-docker2 is installed and configured."
else
    echo "✅ NVIDIA Docker support available"
fi
echo ""

# Build the Docker image
echo "3. Building Docker image (this may take several minutes)..."
docker build -t neuroforge3d:sprint1-test .
echo "✅ Docker image built successfully"
echo ""

# Test the container
echo "4. Testing container..."
docker run --rm neuroforge3d:sprint1-test python3 -c "
import sys
print(f'Python version: {sys.version}')

# Check PyTorch
import torch
print(f'PyTorch version: {torch.__version__}')
print(f'CUDA available: {torch.cuda.is_available()}')
if torch.cuda.is_available():
    print(f'CUDA version: {torch.version.cuda}')
    print(f'GPU count: {torch.cuda.device_count()}')

# Check key dependencies
import trimesh
print(f'Trimesh version: {trimesh.__version__}')

import transformers
print(f'Transformers version: {transformers.__version__}')

import gradio
print(f'Gradio version: {gradio.__version__}')

print('✅ All core dependencies loaded successfully!')
"
echo ""

echo "==================================="
echo "✅ Validation Complete!"
echo "==================================="
echo ""
echo "Next steps:"
echo "1. Run 'docker-compose up -d' to start the development container"
echo "2. Run 'docker-compose exec neuroforge3d bash' to enter the container"
echo "3. Start developing in the /app directory"
echo ""
