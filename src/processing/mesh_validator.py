"""
Mesh validation utilities for 3D printing quality checks.

This module provides comprehensive validation for 3D meshes to ensure
they meet the requirements for successful 3D printing.
"""

import trimesh
import logging
from typing import Dict, List, Any

logger = logging.getLogger(__name__)


def validate_for_printing(mesh: trimesh.Trimesh) -> Dict[str, Any]:
    """
    Validate a mesh for 3D printing suitability.

    Performs comprehensive checks to determine if a mesh is suitable for
    3D printing. This includes checking for watertightness, valid volume,
    disconnected components, and other common issues.

    Args:
        mesh: The Trimesh object to validate.

    Returns:
        Dictionary containing validation results:
            - is_valid (bool): Overall validation result. True if mesh passes
                             all critical checks.
            - errors (List[str]): List of critical errors that prevent printing.
            - warnings (List[str]): List of non-critical issues to be aware of.
            - stats (Dict): Mesh statistics including:
                - volume_mm3 (float): Volume in cubic millimeters
                - area_mm2 (float): Surface area in square millimeters
                - vertices (int): Number of vertices
                - faces (int): Number of faces
                - is_watertight (bool): Whether mesh is watertight
                - body_count (int): Number of disconnected components

    Note:
        The most critical check is watertightness. A mesh that is not watertight
        will fail validation and cannot be reliably 3D printed.

    Example:
        >>> result = validate_for_printing(mesh)
        >>> if result["is_valid"]:
        ...     print("Mesh is ready for printing!")
        ... else:
        ...     print("Errors:", result["errors"])
    """
    if not isinstance(mesh, trimesh.Trimesh):
        return {
            "is_valid": False,
            "errors": [f"Invalid type: expected Trimesh, got {type(mesh).__name__}"],
            "warnings": [],
            "stats": {},
        }

    errors: List[str] = []
    warnings: List[str] = []

    # Critical check: Has geometry (check before other operations)
    if len(mesh.vertices) == 0:
        errors.append("Mesh has no vertices")

    if len(mesh.faces) == 0:
        errors.append("Mesh has no faces")

    # If mesh is empty, return early to avoid errors in other checks
    if len(mesh.vertices) == 0 or len(mesh.faces) == 0:
        stats = {
            "volume_mm3": 0.0,
            "area_mm2": 0.0,
            "vertices": len(mesh.vertices),
            "faces": len(mesh.faces),
            "is_watertight": False,
            "body_count": 0,
        }
        return {
            "is_valid": False,
            "errors": errors,
            "warnings": warnings,
            "stats": stats,
        }

    # Critical check 1: Watertight (GOLDEN RULE)
    is_watertight = mesh.is_watertight
    if not is_watertight:
        errors.append(
            "Mesh is not watertight. Every edge must be shared by exactly "
            "two faces to form a closed volume suitable for 3D printing."
        )

    # Critical check 2: Valid volume
    try:
        volume = mesh.volume
        if volume <= 0:
            errors.append(
                f"Invalid volume: {volume:.4f} mm³. Volume must be positive "
                f"for a valid solid object."
            )
    except Exception as e:
        errors.append(f"Could not calculate volume: {e}")
        volume = 0.0

    # Warning 1: Multiple disconnected components
    try:
        body_count = mesh.body_count
        if body_count > 1:
            warnings.append(
                f"Mesh has {body_count} disconnected components. "
                f"This may cause issues during printing or require separate prints."
            )
    except Exception as e:
        logger.debug(f"Could not get body count: {e}")
        body_count = 1  # Assume single body if check fails

    # Warning 2: Very small volume
    if 0 < volume < 1.0:  # Less than 1 cubic millimeter
        warnings.append(
            f"Very small volume ({volume:.4f} mm³). "
            f"Model may be too small for reliable printing."
        )

    # Warning 3: Very large number of faces (may be over-detailed)
    if len(mesh.faces) > 500000:
        warnings.append(
            f"High polygon count ({len(mesh.faces)} faces). "
            f"Consider decimating the mesh to reduce file size and "
            f"improve slicing performance."
        )

    # Warning 4: Degenerate faces
    try:
        if hasattr(mesh, "face_normals"):
            # Check for zero-area faces
            face_areas = mesh.area_faces
            zero_area_count = (face_areas < 1e-10).sum()
            if zero_area_count > 0:
                warnings.append(
                    f"Found {zero_area_count} degenerate (zero-area) faces. "
                    f"These should be removed."
                )
    except Exception as e:
        logger.debug(f"Could not check for degenerate faces: {e}")

    # Calculate statistics
    try:
        area = mesh.area
    except Exception as e:
        logger.debug(f"Could not calculate area: {e}")
        area = 0.0

    stats = {
        "volume_mm3": float(volume),
        "area_mm2": float(area),
        "vertices": len(mesh.vertices),
        "faces": len(mesh.faces),
        "is_watertight": is_watertight,
        "body_count": body_count,
    }

    # Overall validation result
    is_valid = len(errors) == 0

    # Log results
    if is_valid:
        logger.info(
            f"✓ Mesh validation passed: watertight={is_watertight}, "
            f"volume={volume:.2f}mm³, {len(mesh.faces)} faces"
        )
        if warnings:
            logger.info(f"Warnings: {len(warnings)} non-critical issues found")
    else:
        logger.error(
            f"✗ Mesh validation failed with {len(errors)} error(s): "
            f"{'; '.join(errors[:2])}"  # Log first 2 errors
        )

    return {
        "is_valid": is_valid,
        "errors": errors,
        "warnings": warnings,
        "stats": stats,
    }
