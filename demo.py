#!/usr/bin/env python3
"""
Demo script for NeuroForge 3D.

Demonstrates the core functionality including:
- Mock mesh generation
- Watertight validation
- Processing pipeline
"""

import logging
from pathlib import Path

from src.core.mock_generator import MockGenerator
from src.processing.pipeline import ProcessingPipeline

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """Run demonstration of NeuroForge 3D core functionality."""
    logger.info("=" * 60)
    logger.info("NeuroForge 3D - Demo Script")
    logger.info("=" * 60)

    # Create output directory
    output_dir = Path("outputs")
    output_dir.mkdir(exist_ok=True)

    # Demo 1: Basic generation with MockGenerator
    logger.info("\n### Demo 1: Basic Mesh Generation ###")
    gen = MockGenerator(shape="box", size_mm=50.0)
    result = gen.generate("a simple cube", output_dir / "demo_cube.stl")

    if result["success"]:
        logger.info(f"✓ Generated watertight cube: {result['output_path']}")
        logger.info(f"  Watertight: {result['is_watertight']}")
        logger.info(f"  Vertices: {len(result['mesh'].vertices)}")
        logger.info(f"  Faces: {len(result['mesh'].faces)}")
    else:
        logger.error(f"✗ Generation failed: {result.get('error', 'Unknown error')}")

    # Demo 2: Generate different shapes
    logger.info("\n### Demo 2: Generate Different Shapes ###")
    shapes = ["box", "sphere", "cylinder"]

    for shape in shapes:
        gen = MockGenerator(shape=shape, size_mm=40.0)
        output_path = output_dir / f"demo_{shape}.stl"
        result = gen.generate(f"a {shape}", output_path)

        if result["success"]:
            logger.info(f"✓ Generated {shape}: {output_path.name}")
        else:
            logger.error(f"✗ Failed to generate {shape}")

    # Demo 3: Processing pipeline
    logger.info("\n### Demo 3: Processing Pipeline ###")
    import trimesh

    # Create a large mesh that needs scaling
    large_mesh = trimesh.creation.box(extents=[200, 200, 200])
    logger.info(f"Original mesh size: 200mm x 200mm x 200mm")

    # Process with pipeline
    pipeline = ProcessingPipeline(target_size_mm=100.0, auto_scale=True)
    result = pipeline.process(large_mesh, output_dir / "demo_scaled.stl")

    if result["is_valid"]:
        logger.info(f"✓ Pipeline processed successfully")
        logger.info(f"  Final size: ~100mm (largest dimension)")
        logger.info(f"  Volume: {result['stats']['volume_mm3']:.2f} mm³")
        logger.info(f"  Watertight: {result['stats']['is_watertight']}")
    else:
        logger.error(f"✗ Pipeline failed: {result['errors']}")

    # Demo 4: Validation (showing the golden rule)
    logger.info("\n### Demo 4: Watertight Validation (Golden Rule) ###")
    from src.processing.mesh_validator import validate_for_printing

    # Valid mesh
    valid_mesh = trimesh.creation.box(extents=[10, 10, 10])
    validation = validate_for_printing(valid_mesh)

    logger.info("Valid mesh validation:")
    logger.info(f"  Is valid: {validation['is_valid']}")
    logger.info(f"  Is watertight: {validation['stats']['is_watertight']}")
    logger.info(f"  Errors: {len(validation['errors'])}")
    logger.info(f"  Warnings: {len(validation['warnings'])}")

    logger.info("\n" + "=" * 60)
    logger.info("Demo completed! Check the 'outputs/' directory for STL files.")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
