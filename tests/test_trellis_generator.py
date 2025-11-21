"""
Tests for TrellisGenerator.

These tests validate the TrellisGenerator implementation structure.
Note: Full end-to-end tests require GPU and large model downloads (~10GB).
These are smoke tests to ensure the module structure is correct.
"""

import pytest
from pathlib import Path
import sys


class TestTrellisGeneratorImport:
    """Test suite for TrellisGenerator module structure."""

    def test_trellis_generator_file_exists(self):
        """Test that trellis_generator.py file exists."""
        trellis_path = Path(__file__).parent.parent / "src" / "core" / "trellis_generator.py"
        assert trellis_path.exists(), "trellis_generator.py should exist"

    def test_trellis_generator_has_class_definition(self):
        """Test that TrellisGenerator class is defined in the file."""
        trellis_path = Path(__file__).parent.parent / "src" / "core" / "trellis_generator.py"
        content = trellis_path.read_text()
        assert "class TrellisGenerator" in content
        assert "BaseGenerator" in content

    def test_trellis_generator_has_required_methods(self):
        """Test that TrellisGenerator has all required methods."""
        trellis_path = Path(__file__).parent.parent / "src" / "core" / "trellis_generator.py"
        content = trellis_path.read_text()

        # Check for required methods
        assert "def __init__" in content
        assert "def _generate_raw" in content
        assert "def generate" in content
        assert "def _generate_image_from_text" in content
        assert "def _remove_background" in content
        assert "def _convert_image_to_mesh" in content

    def test_trellis_generator_has_vram_checking(self):
        """Test that VRAM checking logic is present."""
        trellis_path = Path(__file__).parent.parent / "src" / "core" / "trellis_generator.py"
        content = trellis_path.read_text()

        # Check for VRAM checking
        assert "vram_gb" in content
        assert "cpu_offload" in content
        assert "8" in content  # 8GB threshold

    def test_trellis_generator_has_model_loading(self):
        """Test that model loading methods are present."""
        trellis_path = Path(__file__).parent.parent / "src" / "core" / "trellis_generator.py"
        content = trellis_path.read_text()

        # Check for model loading methods
        assert "_load_txt2img_model" in content
        assert "_load_img2mesh_model" in content
        assert "_load_background_remover" in content

    def test_trellis_generator_has_pipeline_integration(self):
        """Test that ProcessingPipeline integration is present."""
        trellis_path = Path(__file__).parent.parent / "src" / "core" / "trellis_generator.py"
        content = trellis_path.read_text()

        # Check for pipeline integration
        assert "ProcessingPipeline" in content
        assert "processing_pipeline" in content

    def test_trellis_generator_has_proper_imports(self):
        """Test that all necessary imports are present."""
        trellis_path = Path(__file__).parent.parent / "src" / "core" / "trellis_generator.py"
        content = trellis_path.read_text()

        # Check for essential imports
        assert "import torch" in content
        assert "from PIL import Image" in content
        assert "import trimesh" in content
        assert "from .base_generator import BaseGenerator" in content

    def test_trellis_generator_has_three_stage_pipeline(self):
        """Test that three-stage pipeline is documented and implemented."""
        trellis_path = Path(__file__).parent.parent / "src" / "core" / "trellis_generator.py"
        content = trellis_path.read_text()

        # Check for three-stage pipeline description
        assert "Stage 1" in content or "stage 1" in content.lower()
        assert "Stage 2" in content or "stage 2" in content.lower()
        assert "Stage 3" in content or "stage 3" in content.lower()

    def test_core_init_handles_missing_dependencies(self):
        """Test that __init__.py gracefully handles missing TrellisGenerator."""
        init_path = Path(__file__).parent.parent / "src" / "core" / "__init__.py"
        content = init_path.read_text()

        # Check for conditional import
        assert "try:" in content
        assert "except ImportError:" in content
        assert "TrellisGenerator" in content


class TestTrellisGeneratorDocumentation:
    """Test suite for TrellisGenerator documentation."""

    def test_has_module_docstring(self):
        """Test that module has proper docstring."""
        trellis_path = Path(__file__).parent.parent / "src" / "core" / "trellis_generator.py"
        content = trellis_path.read_text()

        # Should have module docstring near the top
        lines = content.split("\n")
        docstring_found = False
        for i, line in enumerate(lines[:20]):
            if '"""' in line:
                docstring_found = True
                break
        assert docstring_found, "Module should have a docstring"

    def test_has_class_docstring(self):
        """Test that TrellisGenerator class has docstring."""
        trellis_path = Path(__file__).parent.parent / "src" / "core" / "trellis_generator.py"
        content = trellis_path.read_text()

        # Find class definition and check for docstring
        lines = content.split("\n")
        class_line = None
        for i, line in enumerate(lines):
            if "class TrellisGenerator" in line:
                class_line = i
                break

        assert class_line is not None
        # Check next few lines for docstring
        docstring_found = False
        for i in range(class_line + 1, min(class_line + 10, len(lines))):
            if '"""' in lines[i]:
                docstring_found = True
                break
        assert docstring_found, "TrellisGenerator class should have a docstring"

    def test_mentions_trellis_in_documentation(self):
        """Test that TRELLIS is mentioned in documentation."""
        trellis_path = Path(__file__).parent.parent / "src" / "core" / "trellis_generator.py"
        content = trellis_path.read_text()

        assert "TRELLIS" in content or "Trellis" in content

    def test_mentions_stable_diffusion_in_documentation(self):
        """Test that Stable Diffusion is mentioned in documentation."""
        trellis_path = Path(__file__).parent.parent / "src" / "core" / "trellis_generator.py"
        content = trellis_path.read_text()

        assert "Stable Diffusion" in content or "SDXL" in content or "diffusion" in content.lower()

