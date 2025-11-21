"""
Base generator abstract class for 3D model generation.

This module provides the abstract interface that all 3D model generators
must implement. It enforces the golden rule: all meshes must be validated
with mesh.is_watertight before saving.
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, Any
import trimesh
import logging

logger = logging.getLogger(__name__)


class BaseGenerator(ABC):
    """
    Abstract base class for Text-to-3D generators.

    This class defines the interface that all 3D model generators must implement.
    It enforces watertight mesh validation before saving, ensuring all generated
    models are suitable for 3D printing.

    The generate workflow:
    1. Call _generate_raw() to create the initial mesh
    2. Automatically validate the mesh with validate_mesh()
    3. Only save if validation passes

    Attributes:
        None (subclasses may define their own)
    """

    @abstractmethod
    def _generate_raw(self, prompt: str) -> trimesh.Trimesh:
        """
        Generate a raw 3D mesh from a text prompt.

        This method must be implemented by subclasses to perform the actual
        mesh generation. The returned mesh may not be watertight and will
        be validated before saving.

        Args:
            prompt: Text description of the 3D model to generate.

        Returns:
            A Trimesh object representing the generated 3D model.
            The mesh may not be watertight at this stage.

        Raises:
            NotImplementedError: If the subclass does not implement this method.
            RuntimeError: If mesh generation fails for any reason.
        """
        pass

    def validate_mesh(self, mesh: trimesh.Trimesh) -> bool:
        """
        Validate that a mesh is suitable for 3D printing.

        This method enforces the golden rule: all meshes must be watertight
        before saving. A watertight mesh is one where every edge is shared by
        exactly two faces, creating a closed volume.

        Args:
            mesh: The Trimesh object to validate.

        Returns:
            True if the mesh is watertight and suitable for printing,
            False otherwise.

        Note:
            This is the critical validation step that ensures all generated
            models are printable. Additional validation criteria may be added
            by subclasses.
        """
        if not isinstance(mesh, trimesh.Trimesh):
            logger.error("Invalid mesh type: expected trimesh.Trimesh")
            return False

        is_valid = mesh.is_watertight

        if not is_valid:
            logger.warning(
                f"Mesh validation failed: mesh is not watertight. "
                f"Vertices: {len(mesh.vertices)}, Faces: {len(mesh.faces)}"
            )
        else:
            logger.info(
                f"Mesh validation passed: watertight mesh with "
                f"{len(mesh.vertices)} vertices and {len(mesh.faces)} faces"
            )

        return is_valid

    def generate(self, prompt: str, output_path: Path) -> Dict[str, Any]:
        """
        Generate a 3D model and save it to disk.

        This method orchestrates the complete generation workflow:
        1. Generate raw mesh using _generate_raw()
        2. Validate the mesh is watertight
        3. Save only if validation passes

        Args:
            prompt: Text description of the 3D model to generate.
            output_path: Path where the STL file will be saved.
                        Must use pathlib.Path, not strings.

        Returns:
            Dictionary containing:
                - success (bool): Whether generation succeeded
                - mesh (trimesh.Trimesh): Generated mesh (if successful)
                - output_path (Path): Path where mesh was saved (if successful)
                - error (str): Error message (if failed)
                - is_watertight (bool): Validation result

        Raises:
            TypeError: If output_path is not a Path object.

        Example:
            >>> from pathlib import Path
            >>> generator = MockGenerator()
            >>> result = generator.generate("a cube", Path("outputs/cube.stl"))
            >>> if result["success"]:
            ...     print(f"Saved to {result['output_path']}")
        """
        if not isinstance(output_path, Path):
            raise TypeError(
                f"output_path must be pathlib.Path, not {type(output_path).__name__}"
            )

        logger.info(f"Starting generation with prompt: '{prompt}'")

        try:
            # Generate raw mesh
            mesh = self._generate_raw(prompt)

            # Validate mesh (GOLDEN RULE: must be watertight)
            is_watertight = self.validate_mesh(mesh)

            if not is_watertight:
                error_msg = (
                    "Generated mesh is not watertight and cannot be saved. "
                    "The mesh must be repaired before it can be used for 3D printing."
                )
                logger.error(error_msg)
                return {
                    "success": False,
                    "error": error_msg,
                    "is_watertight": False,
                    "mesh": mesh,
                }

            # Ensure output directory exists
            output_path.parent.mkdir(parents=True, exist_ok=True)

            # Save mesh
            mesh.export(str(output_path))
            logger.info(f"Successfully saved watertight mesh to {output_path}")

            return {
                "success": True,
                "mesh": mesh,
                "output_path": output_path,
                "is_watertight": True,
            }

        except Exception as e:
            error_msg = f"Generation failed: {str(e)}"
            logger.error(error_msg, exc_info=True)
            return {"success": False, "error": error_msg, "is_watertight": False}
