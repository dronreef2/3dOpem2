"""
Processing module for mesh manipulation and validation.

This module provides utilities for repairing, scaling, and validating
3D meshes to ensure they are suitable for 3D printing.
"""

from .mesh_repair import repair_mesh
from .mesh_scaling import normalize_scale
from .mesh_validator import validate_for_printing
from .pipeline import ProcessingPipeline

__all__ = [
    "repair_mesh",
    "normalize_scale",
    "validate_for_printing",
    "ProcessingPipeline",
]
