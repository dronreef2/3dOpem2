"""
Tests for the Gradio UI app.

These tests verify the basic functionality of the NeuroForge Gradio interface.
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
import tempfile
import shutil


class TestNeuroForgeApp(unittest.TestCase):
    """Test cases for NeuroForgeApp class."""

    def setUp(self):
        """Set up test fixtures."""
        # Create a temporary output directory
        self.test_dir = tempfile.mkdtemp()
        self.output_dir = Path(self.test_dir) / "outputs"
        self.output_dir.mkdir()

    def tearDown(self):
        """Clean up test fixtures."""
        if Path(self.test_dir).exists():
            shutil.rmtree(self.test_dir)

    @patch("src.ui.app.OUTPUT_DIR")
    @patch("src.ui.app.TrellisGenerator")
    def test_app_initialization(self, mock_trellis, mock_output_dir):
        """Test that the app can be initialized without errors."""
        # Import here to avoid loading Gradio when not needed
        from src.ui.app import NeuroForgeApp

        mock_output_dir.return_value = self.output_dir

        # Create app instance
        app = NeuroForgeApp()

        # Verify initial state
        self.assertIsNone(app.generator)

    @patch("src.ui.app.OUTPUT_DIR")
    @patch("src.ui.app.TrellisGenerator")
    def test_generator_lazy_initialization(self, mock_trellis, mock_output_dir):
        """Test that the generator is lazily initialized."""
        from src.ui.app import NeuroForgeApp

        mock_output_dir.return_value = self.output_dir

        app = NeuroForgeApp()

        # Generator should be None initially
        self.assertIsNone(app.generator)

        # Initialize generator
        app._initialize_generator(target_size_mm=100.0)

        # Generator should be created
        mock_trellis.assert_called_once_with(target_size_mm=100.0)
        self.assertIsNotNone(app.generator)

    @patch("src.ui.app.OUTPUT_DIR")
    @patch("src.ui.app.TrellisGenerator")
    def test_generate_3d_model_empty_prompt(self, mock_trellis, mock_output_dir):
        """Test that empty prompts are rejected with appropriate error."""
        from src.ui.app import NeuroForgeApp

        mock_output_dir.return_value = self.output_dir

        app = NeuroForgeApp()

        # Mock progress
        mock_progress = MagicMock()

        # Test empty prompt
        result = app.generate_3d_model("", 100.0, None, mock_progress)

        # Should return error
        self.assertIsNone(result[0])  # model_output
        self.assertIsNone(result[1])  # file_output
        self.assertIn("enter a text prompt", result[2].lower())  # status message

    @patch("src.ui.app.OUTPUT_DIR")
    @patch("src.ui.app.TrellisGenerator")
    def test_generate_3d_model_invalid_size(self, mock_trellis, mock_output_dir):
        """Test that invalid sizes are rejected."""
        from src.ui.app import NeuroForgeApp

        mock_output_dir.return_value = self.output_dir

        app = NeuroForgeApp()

        # Mock progress
        mock_progress = MagicMock()

        # Test size too large
        result = app.generate_3d_model("a cube", 1000.0, None, mock_progress)

        # Should return error
        self.assertIsNone(result[0])
        self.assertIsNone(result[1])
        self.assertIn("target size", result[2].lower())

        # Test negative size
        result = app.generate_3d_model("a cube", -10.0, None, mock_progress)

        # Should return error
        self.assertIsNone(result[0])
        self.assertIsNone(result[1])
        self.assertIn("target size", result[2].lower())

    @patch("src.ui.app.OUTPUT_DIR")
    @patch("src.ui.app.TrellisGenerator")
    def test_generate_3d_model_success(self, mock_trellis, mock_output_dir):
        """Test successful 3D model generation."""
        from src.ui.app import NeuroForgeApp
        import trimesh

        mock_output_dir.return_value = self.output_dir

        app = NeuroForgeApp()

        # Mock the generator
        mock_gen = Mock()
        mock_mesh = trimesh.creation.box(extents=[10, 10, 10])
        mock_gen.generate.return_value = {
            "success": True,
            "mesh": mock_mesh,
            "output_path": self.output_dir / "test.stl",
            "is_watertight": True,
            "pipeline_stats": {
                "volume_mm3": 1000.0,
            },
        }
        mock_trellis.return_value = mock_gen

        # Mock progress
        mock_progress = MagicMock()

        # Generate model
        result = app.generate_3d_model("a cube", 100.0, None, mock_progress)

        # Should succeed
        self.assertIsNotNone(result[0])  # model_output path
        self.assertIsNotNone(result[1])  # file_output path
        self.assertIn("successful", result[2].lower())  # status message

    @patch("src.ui.app.OUTPUT_DIR")
    @patch("src.ui.app.TrellisGenerator")
    def test_generate_3d_model_failure(self, mock_trellis, mock_output_dir):
        """Test failed 3D model generation."""
        from src.ui.app import NeuroForgeApp

        mock_output_dir.return_value = self.output_dir

        app = NeuroForgeApp()

        # Mock the generator to fail
        mock_gen = Mock()
        mock_gen.generate.return_value = {
            "success": False,
            "error": "Model generation failed",
            "is_watertight": False,
        }
        mock_trellis.return_value = mock_gen

        # Mock progress
        mock_progress = MagicMock()

        # Attempt to generate model
        result = app.generate_3d_model("a cube", 100.0, None, mock_progress)

        # Should fail gracefully
        self.assertIsNone(result[0])  # model_output
        self.assertIsNone(result[1])  # file_output
        self.assertIn("failed", result[2].lower())  # status message

    @patch("src.ui.app.gr")
    @patch("src.ui.app.OUTPUT_DIR")
    def test_create_interface(self, mock_output_dir, mock_gr):
        """Test that the interface can be created."""
        from src.ui.app import NeuroForgeApp

        mock_output_dir.return_value = self.output_dir

        # Mock Gradio components
        mock_blocks = MagicMock()
        mock_gr.Blocks.return_value.__enter__.return_value = mock_blocks

        app = NeuroForgeApp()

        # Should not raise any errors
        interface = app.create_interface()

        # Verify Gradio Blocks was created
        mock_gr.Blocks.assert_called_once()


class TestLaunchUI(unittest.TestCase):
    """Test cases for launch_ui.py script."""

    def test_launch_ui_import(self):
        """Test that launch_ui.py can be imported without errors."""
        # This is a simple syntax check
        import launch_ui

        self.assertTrue(hasattr(launch_ui, "main"))


if __name__ == "__main__":
    unittest.main()
