# NeuroForge 3D - SPRINT 1 Optimized Multi-Stage Dockerfile
# Text-to-Printable-3D using Microsoft TRELLIS
# Base: NVIDIA CUDA 12.1 (as specified in PROJECT_CONTEXT.md)
# Architecture: Multi-stage build for reduced image size

# ============================================================================
# STAGE 1: BUILDER - Compile dependencies and install packages
# ============================================================================
FROM nvidia/cuda:12.1.0-devel-ubuntu22.04 AS builder

# Build argument to control PyTorch installation type (cuda or cpu)
ARG PYTORCH_VARIANT=cuda

# Prevent interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

# Install build dependencies and Python
RUN apt-get update && apt-get install -y \
    python3.10 \
    python3-pip \
    python3.10-dev \
    build-essential \
    git \
    wget \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip and install build tools
RUN python3 -m pip install --no-cache-dir --upgrade pip setuptools wheel

# Set working directory for build
WORKDIR /build

# Copy requirements file first (for Docker layer caching)
COPY requirements.txt /build/requirements.txt

# Install PyTorch with CPU-only support
RUN --mount=type=cache,target=/root/.cache/pip \
    pip3 install --no-cache-dir \
    torch==2.4.0 \
    torchvision==0.19.0 \
    --index-url https://download.pytorch.org/whl/cpu

# Install xformers for attention mechanisms (CPU-compatible)
RUN --mount=type=cache,target=/root/.cache/pip \
    pip3 install --no-cache-dir \
    xformers==0.0.27.post2 \
    --index-url https://download.pytorch.org/whl/cpu

# Install all other Python dependencies with pip cache mounting
RUN --mount=type=cache,target=/root/.cache/pip \
    pip3 install --no-cache-dir -r /build/requirements.txt

# ============================================================================
# STAGE 2: RUNTIME - Minimal runtime environment
# ============================================================================
FROM nvidia/cuda:12.1.0-runtime-ubuntu22.04 AS runtime

# Pass build argument to runtime stage
ARG PYTORCH_VARIANT=cuda

# Prevent interactive prompts
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

# Install only runtime dependencies (no build tools)
RUN apt-get update && apt-get install -y \
    python3.10 \
    python3-pip \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    libjpeg-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy Python packages from builder stage
COPY --from=builder /usr/local/lib/python3.10/dist-packages /usr/local/lib/python3.10/dist-packages

# Copy only Python-related executables from builder
# This is more selective than copying all of /usr/local/bin
COPY --from=builder /usr/local/bin/python* /usr/local/bin/
COPY --from=builder /usr/local/bin/pip* /usr/local/bin/

# Copy application source code
COPY src/ /app/src/
COPY demo.py /app/demo.py
COPY validate_docker.sh /app/validate_docker.sh

# Create directories for models and outputs
RUN mkdir -p /app/models /app/outputs

# Set Python path
ENV PYTHONPATH=/app:$PYTHONPATH

# Environment variables for TRELLIS compatibility
ENV ATTN_BACKEND=xformers
ENV SPCONV_ALGO=native

# Expose port for Gradio (SPRINT 4)
EXPOSE 7860

# Default command (can be overridden)
CMD ["/bin/bash"]

# Health check (verify Python and PyTorch are working)
# Updated for CPU-only deployment compatibility
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python3 -c "import torch; torch.zeros(1)" || exit 1

# Labels for documentation
LABEL maintainer="NeuroForge 3D Team"
LABEL description="Docker image for NeuroForge 3D - Text-to-Printable-3D using TRELLIS"
LABEL version="sprint-1"
LABEL org.opencontainers.image.source="https://github.com/dronreef2/3dOpem2"
