# NeuroForge 3D - SPRINT 1 Dockerfile
# Text-to-Printable-3D using Microsoft TRELLIS
# Base: NVIDIA CUDA 12.1 (as specified in PROJECT_CONTEXT.md)

FROM nvidia/cuda:12.1.0-devel-ubuntu22.04

# Prevent interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3.10 \
    python3-pip \
    python3.10-dev \
    git \
    wget \
    curl \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    libjpeg-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN python3 -m pip install --upgrade pip setuptools wheel

# Install PyTorch with CUDA 12.1 support
RUN pip3 install torch==2.4.0 torchvision==0.19.0 --index-url https://download.pytorch.org/whl/cu121

# Copy requirements file
COPY requirements.txt /app/requirements.txt

# Install Python dependencies
RUN pip3 install -r /app/requirements.txt

# Install additional CUDA-dependent packages for TRELLIS
# xformers for attention mechanisms
RUN pip3 install xformers==0.0.27.post2 --index-url https://download.pytorch.org/whl/cu121

# Create directories for future code
RUN mkdir -p /app/src/core /app/models /app/outputs

# Set Python path
ENV PYTHONPATH=/app:$PYTHONPATH

# Environment variables for TRELLIS compatibility
ENV ATTN_BACKEND=xformers
ENV SPCONV_ALGO=native

# Default command (can be overridden)
CMD ["/bin/bash"]

# Health check (optional, for future web service)
# HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
#   CMD python3 -c "import torch; print(torch.cuda.is_available())" || exit 1

# Expose port for Gradio (SPRINT 4)
EXPOSE 7860

# Labels for documentation
LABEL maintainer="NeuroForge 3D Team"
LABEL description="Docker image for NeuroForge 3D - Text-to-Printable-3D using TRELLIS"
LABEL version="sprint-1"
