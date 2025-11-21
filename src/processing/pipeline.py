"""
Complete processing pipeline for 3D mesh preparation.

This module provides an integrated pipeline that combines repair, scaling,
and validation to prepare meshes for 3D printing.
"""

from pathlib import Path
from typing import Dict, Any, Optional
import trimesh
import logging

from .mesh_repair import repair_mesh
from .mesh_scaling import normalize_scale
from .mesh_validator import validate_for_printing

logger = logging.getLogger(__name__)


class ProcessingPipeline:
    """
    Complete pipeline for processing 3D meshes for printing.

    This pipeline integrates mesh repair, scaling, and validation into a
    single workflow. It ensures that all output meshes are watertight and
    suitable for 3D printing.

    Pipeline steps:
    1. Repair mesh (fill holes, fix normals, remove small components)
    2. Normalize scale to target size
    3. Validate for printing (watertight check, volume check, etc.)
    4. Save only if validation passes

    Attributes:
        target_size_mm: Target size for mesh normalization in millimeters.
        auto_repair: Whether to automatically repair non-watertight meshes.
        auto_scale: Whether to automatically scale meshes to target size.

    Example:
        >>> pipeline = ProcessingPipeline(target_size_mm=100.0)
        >>> result = pipeline.process(raw_mesh, Path("outputs/model.stl"))
        >>> if result["is_valid"]:
        ...     print(f"Saved to {result['output_path']}")
    """

    def __init__(
        self,
        target_size_mm: float = 100.0,
        auto_repair: bool = True,
        auto_scale: bool = True,
    ) -> None:
        """
        Initialize the processing pipeline.

        Args:
            target_size_mm: Target size in millimeters for the largest dimension
                          of the mesh after normalization.
            auto_repair: If True, automatically attempt to repair non-watertight
                        meshes before validation.
            auto_scale: If True, automatically scale meshes to target_size_mm.
                       If False, mesh dimensions are preserved.
        """
        self.target_size_mm = target_size_mm
        self.auto_repair = auto_repair
        self.auto_scale = auto_scale

        logger.info(
            f"Initialized ProcessingPipeline: "
            f"target_size={target_size_mm}mm, "
            f"auto_repair={auto_repair}, "
            f"auto_scale={auto_scale}"
        )

    def process(
        self, mesh: trimesh.Trimesh, output_path: Optional[Path] = None
    ) -> Dict[str, Any]:
        """
        Process a mesh through the complete pipeline.

        Executes the full processing workflow: repair, scale, validate, and
        optionally save. The mesh is only saved if it passes all validation
        checks (especially watertightness).

        Args:
            mesh: The input Trimesh object to process.
            output_path: Optional path where to save the processed mesh.
                        If None, mesh is processed but not saved.
                        Must be a pathlib.Path object.

        Returns:
            Dictionary containing:
                - is_valid (bool): Whether the mesh passed validation
                - errors (List[str]): List of validation errors
                - warnings (List[str]): List of validation warnings
                - stats (Dict): Mesh statistics
                - output_path (Path): Where mesh was saved (if provided and valid)
                - mesh (trimesh.Trimesh): The processed mesh
                - repaired (bool): Whether repair was applied
                - scaled (bool): Whether scaling was applied

        Raises:
            TypeError: If mesh is not a Trimesh or output_path is not a Path.

        Note:
            The pipeline enforces the golden rule: meshes are only saved if
            they are watertight. This ensures all output is suitable for
            3D printing.
        """
        if not isinstance(mesh, trimesh.Trimesh):
            raise TypeError(f"Expected trimesh.Trimesh, got {type(mesh).__name__}")

        if output_path is not None and not isinstance(output_path, Path):
            raise TypeError(
                f"output_path must be pathlib.Path, got {type(output_path).__name__}"
            )

        logger.info("=" * 60)
        logger.info("Starting mesh processing pipeline")
        logger.info("=" * 60)

        # Track what operations were performed
        was_repaired = False
        was_scaled = False

        # Step 1: Repair (if enabled and needed)
        if self.auto_repair:
            if not mesh.is_watertight:
                logger.info("Step 1/3: Repairing mesh...")
                mesh = repair_mesh(mesh)
                was_repaired = True
            else:
                logger.info("Step 1/3: Repair - Skipped (already watertight)")
        else:
            logger.info("Step 1/3: Repair - Disabled")

        # Step 2: Scale (if enabled)
        if self.auto_scale:
            logger.info("Step 2/3: Normalizing scale...")
            mesh = normalize_scale(
                mesh, target_size_mm=self.target_size_mm, dimension="max", center=True
            )
            was_scaled = True
        else:
            logger.info("Step 2/3: Scaling - Disabled")

        # Step 3: Validate
        logger.info("Step 3/3: Validating mesh...")
        validation_result = validate_for_printing(mesh)

        # Add processing metadata to result
        result = {
            **validation_result,
            "mesh": mesh,
            "repaired": was_repaired,
            "scaled": was_scaled,
        }

        # Step 4: Save (if path provided and validation passed)
        if output_path is not None:
            if validation_result["is_valid"]:
                # Ensure output directory exists
                output_path.parent.mkdir(parents=True, exist_ok=True)

                # Save mesh
                mesh.export(str(output_path))
                result["output_path"] = output_path

                logger.info("=" * 60)
                logger.info(f"✓ SUCCESS: Processed mesh saved to {output_path}")
                logger.info(
                    f"  Watertight: {validation_result['stats']['is_watertight']}"
                )
                logger.info(
                    f"  Volume: {validation_result['stats']['volume_mm3']:.2f} mm³"
                )
                logger.info("=" * 60)
            else:
                logger.error("=" * 60)
                logger.error("✗ FAILURE: Mesh validation failed, not saved")
                logger.error(f"  Errors: {', '.join(validation_result['errors'])}")
                logger.error("=" * 60)
        else:
            if validation_result["is_valid"]:
                logger.info("Pipeline completed successfully (no save path provided)")
            else:
                logger.warning("Pipeline completed with validation errors")

        return result
