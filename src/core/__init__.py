"""
Core module for NeuroForge 3D.

Contains base classes and implementations for 3D model generation.
"""

from .base_generator import BaseGenerator
from .mock_generator import MockGenerator

# TrellisGenerator requires additional dependencies (torch, diffusers, etc.)
# Import it conditionally to avoid breaking basic functionality
try:
    from .trellis_generator import TrellisGenerator

    __all__ = ["BaseGenerator", "MockGenerator", "TrellisGenerator"]
except ImportError:
    # TrellisGenerator dependencies not available
    __all__ = ["BaseGenerator", "MockGenerator"]
