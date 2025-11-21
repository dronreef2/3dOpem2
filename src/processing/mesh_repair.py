"""
Mesh repair utilities for fixing non-watertight meshes.

This module provides functions to repair 3D meshes, making them watertight
and suitable for 3D printing.
"""

import trimesh
import logging

logger = logging.getLogger(__name__)


def repair_mesh(
    mesh: trimesh.Trimesh,
    fill_holes: bool = True,
    fix_normals: bool = True,
    remove_small_components: bool = True,
    min_component_ratio: float = 0.05,
) -> trimesh.Trimesh:
    """
    Repair a mesh to make it watertight and suitable for 3D printing.

    This function applies a series of repair operations to fix common issues
    in 3D meshes. The goal is to transform a potentially broken mesh into
    a watertight solid that can be 3D printed.

    Repair steps:
    1. Check if already watertight (early return if yes)
    2. Fill holes in the mesh surface
    3. Fix face normals to point outward
    4. Remove small disconnected components
    5. Keep only the largest watertight component

    Args:
        mesh: The Trimesh object to repair.
        fill_holes: Whether to attempt filling holes in the mesh.
        fix_normals: Whether to fix face normal directions.
        remove_small_components: Whether to remove small disconnected pieces.
        min_component_ratio: Minimum size for components as ratio of vertices.
                           Components with fewer than this fraction of total
                           vertices will be removed. Default: 0.05 (5%).

    Returns:
        Repaired Trimesh object. May be watertight if repair succeeded.

    Note:
        Repair is not guaranteed to succeed for all meshes. Some severely
        broken meshes may require manual intervention. Always check
        is_watertight on the returned mesh.

    Example:
        >>> mesh = load_broken_mesh()
        >>> repaired = repair_mesh(mesh)
        >>> if repaired.is_watertight:
        ...     print("Repair successful!")
    """
    if not isinstance(mesh, trimesh.Trimesh):
        raise TypeError(f"Expected trimesh.Trimesh, got {type(mesh).__name__}")

    # Early return if already watertight
    if mesh.is_watertight:
        logger.info("Mesh is already watertight, no repair needed")
        return mesh

    logger.info(
        f"Starting mesh repair. Initial state: "
        f"{len(mesh.vertices)} vertices, "
        f"{len(mesh.faces)} faces, "
        f"watertight={mesh.is_watertight}"
    )

    # Make a copy to avoid modifying the original
    mesh = mesh.copy()

    # Step 1: Fill holes
    if fill_holes:
        logger.debug("Filling holes...")
        try:
            mesh.fill_holes()
        except Exception as e:
            logger.warning(f"Fill holes failed: {e}")

    # Step 2: Fix normals
    if fix_normals:
        logger.debug("Fixing normals...")
        try:
            mesh.fix_normals()
        except Exception as e:
            logger.warning(f"Fix normals failed: {e}")

    # Step 3: Remove small components
    if remove_small_components and mesh.body_count > 1:
        logger.debug(f"Mesh has {mesh.body_count} components, filtering...")

        # Split into separate components
        components = mesh.split(only_watertight=False)

        # Sort by vertex count (largest first)
        components.sort(key=lambda m: len(m.vertices), reverse=True)

        # Calculate minimum vertices threshold
        total_vertices = sum(len(m.vertices) for m in components)
        min_vertices = int(total_vertices * min_component_ratio)

        # Keep components above threshold
        kept_components = [
            comp for comp in components if len(comp.vertices) >= min_vertices
        ]

        if kept_components:
            # Combine kept components
            if len(kept_components) == 1:
                mesh = kept_components[0]
            else:
                mesh = trimesh.util.concatenate(kept_components)

            logger.debug(f"Kept {len(kept_components)} of {len(components)} components")
        else:
            # Fallback: keep only the largest
            mesh = components[0]
            logger.debug("Kept only the largest component")

    # Final status
    logger.info(
        f"Repair completed. Final state: "
        f"{len(mesh.vertices)} vertices, "
        f"{len(mesh.faces)} faces, "
        f"watertight={mesh.is_watertight}"
    )

    return mesh
