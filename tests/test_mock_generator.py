"""
Tests for MockGenerator.

Validates that the mock generator creates valid watertight meshes.
"""

import pytest
from pathlib import Path
import trimesh
import tempfile
import shutil

from src.core.mock_generator import MockGenerator


class TestMockGenerator:
    """Test suite for MockGenerator class."""

    def setup_method(self):
        """Set up test fixtures before each test."""
        # Create temporary directory for test outputs
        self.test_dir = Path(tempfile.mkdtemp())

    def teardown_method(self):
        """Clean up after each test."""
        # Remove temporary directory
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)

    def test_init_default(self):
        """Test MockGenerator initialization with default parameters."""
        gen = MockGenerator()
        assert gen.shape == "box"
        assert gen.size_mm == 50.0

    def test_init_custom_shape(self):
        """Test MockGenerator initialization with custom shape."""
        gen = MockGenerator(shape="sphere", size_mm=100.0)
        assert gen.shape == "sphere"
        assert gen.size_mm == 100.0

    def test_init_invalid_shape(self):
        """Test that invalid shape raises ValueError."""
        with pytest.raises(ValueError, match="Unsupported shape"):
            MockGenerator(shape="pyramid")

    def test_generate_box(self):
        """Test generating a box mesh."""
        gen = MockGenerator(shape="box", size_mm=50.0)
        output_path = self.test_dir / "box.stl"

        result = gen.generate("test box", output_path)

        assert result["success"] is True
        assert result["is_watertight"] is True
        assert output_path.exists()

        # Verify the saved mesh
        mesh = trimesh.load(str(output_path))
        assert mesh.is_watertight

    def test_generate_sphere(self):
        """Test generating a sphere mesh."""
        gen = MockGenerator(shape="sphere", size_mm=60.0)
        output_path = self.test_dir / "sphere.stl"

        result = gen.generate("test sphere", output_path)

        assert result["success"] is True
        assert result["is_watertight"] is True
        assert output_path.exists()

    def test_generate_cylinder(self):
        """Test generating a cylinder mesh."""
        gen = MockGenerator(shape="cylinder", size_mm=40.0)
        output_path = self.test_dir / "cylinder.stl"

        result = gen.generate("test cylinder", output_path)

        assert result["success"] is True
        assert result["is_watertight"] is True
        assert output_path.exists()

    def test_validate_mesh(self):
        """Test that generated meshes pass validation."""
        gen = MockGenerator(shape="box")
        mesh = gen._generate_raw("test")

        is_valid = gen.validate_mesh(mesh)
        assert is_valid is True

    def test_output_path_must_be_pathlib(self):
        """Test that output_path must be a Path object, not string."""
        gen = MockGenerator()

        with pytest.raises(TypeError, match="must be pathlib.Path"):
            gen.generate("test", "/tmp/test.stl")  # String instead of Path

    def test_creates_output_directory(self):
        """Test that generate creates output directory if it doesn't exist."""
        gen = MockGenerator()
        nested_path = self.test_dir / "subdir1" / "subdir2" / "model.stl"

        result = gen.generate("test", nested_path)

        assert result["success"] is True
        assert nested_path.exists()
        assert nested_path.parent.exists()
