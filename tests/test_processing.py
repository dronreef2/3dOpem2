"""
Tests for processing pipeline.

Validates mesh repair, scaling, and validation functionality.
"""

import pytest
from pathlib import Path
import trimesh
import tempfile
import shutil

from src.processing.pipeline import ProcessingPipeline
from src.processing.mesh_repair import repair_mesh
from src.processing.mesh_scaling import normalize_scale
from src.processing.mesh_validator import validate_for_printing


class TestProcessingPipeline:
    """Test suite for ProcessingPipeline class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.test_dir = Path(tempfile.mkdtemp())

    def teardown_method(self):
        """Clean up after tests."""
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)

    def test_pipeline_valid_mesh(self):
        """Test pipeline with a valid watertight mesh."""
        mesh = trimesh.creation.box(extents=[10, 10, 10])
        pipeline = ProcessingPipeline(target_size_mm=50.0)
        output_path = self.test_dir / "test.stl"

        result = pipeline.process(mesh, output_path)

        assert result["is_valid"] is True
        assert result["stats"]["is_watertight"] is True
        assert output_path.exists()

    def test_pipeline_without_save(self):
        """Test pipeline without saving the mesh."""
        mesh = trimesh.creation.icosphere(subdivisions=3, radius=25)
        pipeline = ProcessingPipeline()

        result = pipeline.process(mesh, output_path=None)

        assert result["is_valid"] is True
        assert "output_path" not in result

    def test_pipeline_scales_mesh(self):
        """Test that pipeline scales mesh to target size."""
        # Create 200mm mesh
        mesh = trimesh.creation.box(extents=[200, 200, 200])
        pipeline = ProcessingPipeline(target_size_mm=100.0, auto_scale=True)

        result = pipeline.process(mesh)

        processed_mesh = result["mesh"]
        bounds = processed_mesh.bounds
        max_dimension = (bounds[1] - bounds[0]).max()

        # Should be approximately 100mm (allow small tolerance)
        assert abs(max_dimension - 100.0) < 0.1
        assert result["scaled"] is True

    def test_pipeline_no_auto_scale(self):
        """Test pipeline with auto_scale disabled."""
        mesh = trimesh.creation.box(extents=[200, 200, 200])
        pipeline = ProcessingPipeline(auto_scale=False)

        result = pipeline.process(mesh)

        processed_mesh = result["mesh"]
        bounds = processed_mesh.bounds
        max_dimension = (bounds[1] - bounds[0]).max()

        # Should still be 200mm
        assert abs(max_dimension - 200.0) < 0.1
        assert result["scaled"] is False


class TestMeshValidator:
    """Test suite for mesh validation."""

    def test_validate_watertight_mesh(self):
        """Test validation of a watertight mesh."""
        mesh = trimesh.creation.box(extents=[10, 10, 10])
        result = validate_for_printing(mesh)

        assert result["is_valid"] is True
        assert len(result["errors"]) == 0
        assert result["stats"]["is_watertight"] is True
        assert result["stats"]["volume_mm3"] > 0

    def test_validate_invalid_type(self):
        """Test validation with invalid input type."""
        result = validate_for_printing("not a mesh")

        assert result["is_valid"] is False
        assert len(result["errors"]) > 0
        assert "Invalid type" in result["errors"][0]

    def test_validate_empty_mesh(self):
        """Test validation of a mesh with no vertices."""
        # Create an empty mesh - trimesh can have issues with completely empty meshes
        # So we check early validation catches this
        mesh = trimesh.Trimesh(vertices=[], faces=[])
        result = validate_for_printing(mesh)

        assert result["is_valid"] is False
        # Should have errors about missing vertices and faces
        assert any("no vertices" in err.lower() for err in result["errors"])


class TestMeshScaling:
    """Test suite for mesh scaling."""

    def test_normalize_scale_max_dimension(self):
        """Test normalizing mesh by maximum dimension."""
        mesh = trimesh.creation.box(extents=[100, 50, 25])
        scaled = normalize_scale(mesh, target_size_mm=50.0, dimension="max")

        bounds = scaled.bounds
        max_dimension = (bounds[1] - bounds[0]).max()

        assert abs(max_dimension - 50.0) < 0.1

    def test_normalize_scale_preserves_aspect_ratio(self):
        """Test that scaling preserves aspect ratio."""
        # Create 2:1:0.5 ratio box
        mesh = trimesh.creation.box(extents=[100, 50, 25])
        scaled = normalize_scale(mesh, target_size_mm=50.0)

        bounds = scaled.bounds
        dimensions = bounds[1] - bounds[0]

        # Check ratios are preserved (approximately)
        assert abs(dimensions[0] / dimensions[1] - 2.0) < 0.01
        assert abs(dimensions[1] / dimensions[2] - 2.0) < 0.01

    def test_normalize_scale_centers_mesh(self):
        """Test that centering option works."""
        mesh = trimesh.creation.box(extents=[10, 10, 10])
        mesh.apply_translation([100, 100, 100])  # Move far from origin

        scaled = normalize_scale(mesh, center=True)

        # Centroid should be at origin
        centroid = scaled.centroid
        assert abs(centroid[0]) < 0.1
        assert abs(centroid[1]) < 0.1
        assert abs(centroid[2]) < 0.1

    def test_normalize_scale_invalid_dimension(self):
        """Test that invalid dimension raises ValueError."""
        mesh = trimesh.creation.box(extents=[10, 10, 10])

        with pytest.raises(ValueError, match="Invalid dimension"):
            normalize_scale(mesh, dimension="invalid")


class TestMeshRepair:
    """Test suite for mesh repair."""

    def test_repair_already_watertight(self):
        """Test that repairing a watertight mesh returns it unchanged."""
        mesh = trimesh.creation.box(extents=[10, 10, 10])
        assert mesh.is_watertight

        repaired = repair_mesh(mesh)

        assert repaired.is_watertight
        # Should be essentially the same mesh
        assert len(repaired.vertices) == len(mesh.vertices)
        assert len(repaired.faces) == len(mesh.faces)

    def test_repair_invalid_type(self):
        """Test that repair raises TypeError for invalid input."""
        with pytest.raises(TypeError, match="Expected trimesh.Trimesh"):
            repair_mesh("not a mesh")
