#!/usr/bin/env python3
"""
Launch script for NeuroForge 3D Gradio web interface.

This script provides a convenient entry point to start the Gradio
web interface for NeuroForge 3D.

Usage:
    python launch_ui.py

    Or with Docker:
    docker run --gpus all -p 7860:7860 neuroforge3d:sprint1 python launch_ui.py
"""

import sys
import logging
from pathlib import Path

# Add src to path if needed
src_path = Path(__file__).parent / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """Launch the Gradio interface."""
    logger.info("=" * 60)
    logger.info("Starting NeuroForge 3D Web Interface")
    logger.info("=" * 60)
    
    try:
        from src.ui.app import main as app_main
        app_main()
    except Exception as e:
        logger.error(f"Failed to start Gradio interface: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
