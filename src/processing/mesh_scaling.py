"""
Mesh scaling utilities for normalizing 3D model dimensions.

This module provides functions to scale and normalize 3D meshes to
standard sizes suitable for 3D printing.
"""

import trimesh
import logging

logger = logging.getLogger(__name__)


def normalize_scale(
    mesh: trimesh.Trimesh,
    target_size_mm: float = 100.0,
    dimension: str = "max",
    center: bool = True,
) -> trimesh.Trimesh:
    """
    Normalize mesh scale to a target size.

    Scales the mesh so that its bounding box matches the specified target
    size. This is useful for standardizing model sizes for 3D printing.

    Args:
        mesh: The Trimesh object to scale.
        target_size_mm: Target size in millimeters. The mesh will be scaled
                       so the specified dimension equals this value.
        dimension: Which dimension to use for scaling:
                  - 'max': Scale based on largest dimension (default)
                  - 'x': Scale based on X dimension
                  - 'y': Scale based on Y dimension
                  - 'z': Scale based on Z dimension
                  - 'min': Scale based on smallest dimension
        center: If True, center the mesh at the origin (0, 0, 0) after scaling.

    Returns:
        Scaled Trimesh object with target dimensions.

    Raises:
        ValueError: If dimension is not one of the supported options.
        TypeError: If mesh is not a Trimesh object.

    Note:
        - Scaling preserves aspect ratio (proportional scaling)
        - Original mesh is not modified (returns a copy)
        - Mesh volume scales with the cube of the scale factor

    Example:
        >>> mesh = load_model()  # 200mm tall
        >>> scaled = normalize_scale(mesh, target_size_mm=50.0, dimension='max')
        >>> # Now largest dimension is 50mm
    """
    if not isinstance(mesh, trimesh.Trimesh):
        raise TypeError(f"Expected trimesh.Trimesh, got {type(mesh).__name__}")

    valid_dimensions = ("max", "min", "x", "y", "z")
    if dimension not in valid_dimensions:
        raise ValueError(
            f"Invalid dimension '{dimension}'. "
            f"Must be one of: {', '.join(valid_dimensions)}"
        )

    # Make a copy to avoid modifying original
    mesh = mesh.copy()

    # Get bounding box
    bounds = mesh.bounds  # [[min_x, min_y, min_z], [max_x, max_y, max_z]]
    current_dimensions = bounds[1] - bounds[0]  # [width, height, depth]

    # Determine which dimension to use for scaling
    if dimension == "max":
        current_size = current_dimensions.max()
        dim_name = "largest"
    elif dimension == "min":
        current_size = current_dimensions.min()
        dim_name = "smallest"
    elif dimension == "x":
        current_size = current_dimensions[0]
        dim_name = "X"
    elif dimension == "y":
        current_size = current_dimensions[1]
        dim_name = "Y"
    elif dimension == "z":
        current_size = current_dimensions[2]
        dim_name = "Z"

    # Calculate scale factor
    if current_size == 0:
        logger.warning(
            f"Current {dim_name} dimension is 0, cannot scale. "
            f"Returning original mesh."
        )
        return mesh

    scale_factor = target_size_mm / current_size

    logger.info(
        f"Scaling mesh: {dim_name} dimension from "
        f"{current_size:.2f}mm to {target_size_mm:.2f}mm "
        f"(factor: {scale_factor:.4f})"
    )

    # Apply scaling
    mesh.apply_scale(scale_factor)

    # Center mesh at origin if requested
    if center:
        centroid = mesh.centroid
        mesh.apply_translation(-centroid)
        logger.debug(f"Centered mesh at origin (moved from {centroid})")

    # Log final dimensions
    final_bounds = mesh.bounds
    final_dimensions = final_bounds[1] - final_bounds[0]
    logger.info(
        f"Final dimensions: "
        f"X={final_dimensions[0]:.2f}mm, "
        f"Y={final_dimensions[1]:.2f}mm, "
        f"Z={final_dimensions[2]:.2f}mm"
    )

    return mesh
