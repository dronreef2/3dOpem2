"""
Examples of using NeuroForge 3D Gradio Interface.

This module demonstrates various ways to use the Gradio web interface
programmatically and through the web UI.
"""

# =============================================================================
# Example 1: Basic Launch
# =============================================================================

def example_basic_launch():
    """
    Simplest way to launch the Gradio interface.
    
    This will start the web UI on http://localhost:7860
    """
    from src.ui.app import NeuroForgeApp
    
    app = NeuroForgeApp()
    app.launch()


# =============================================================================
# Example 2: Custom Configuration
# =============================================================================

def example_custom_launch():
    """
    Launch with custom configuration.
    
    Useful for:
    - Running on different ports
    - Enabling public sharing
    - Custom server settings
    """
    from src.ui.app import NeuroForgeApp
    
    app = NeuroForgeApp()
    app.launch(
        server_name="0.0.0.0",  # Accept connections from any IP
        server_port=8080,        # Custom port
        share=True,              # Create public Gradio URL
        show_error=True          # Show detailed errors
    )


# =============================================================================
# Example 3: Using the UI (Web Browser)
# =============================================================================

"""
Web UI Usage Example:

1. Start the server:
   python launch_ui.py

2. Open browser to http://localhost:7860

3. Enter a prompt:
   "a modern coffee mug with geometric patterns"

4. Configure parameters:
   - Target Size: 100mm
   - Seed: 42 (for reproducible results)

5. Click "Generate 3D Model"

6. Wait 2-5 minutes for generation

7. View the 3D model in the interactive viewer

8. Download the STL file for 3D printing
"""


# =============================================================================
# Example 4: Docker Usage
# =============================================================================

"""
Using NeuroForge UI with Docker:

Method 1 - Docker Compose (Recommended):
    
    docker-compose up
    # Access at http://localhost:7860

Method 2 - Docker Run:
    
    docker run --gpus all -p 7860:7860 \
      -v $(pwd)/outputs:/app/outputs \
      neuroforge3d:sprint1 \
      python launch_ui.py

Method 3 - Docker Run with Custom Port:
    
    docker run --gpus all -p 8080:7860 \
      -v $(pwd)/outputs:/app/outputs \
      neuroforge3d:sprint1 \
      python launch_ui.py

    # Access at http://localhost:8080
"""


# =============================================================================
# Example 5: Programmatic Generation (Without UI)
# =============================================================================

def example_programmatic_generation():
    """
    Generate models programmatically without the web UI.
    
    Useful for:
    - Batch generation
    - Scripting
    - Integration with other tools
    """
    from pathlib import Path
    from src.core.trellis_generator import TrellisGenerator
    
    # Initialize generator
    generator = TrellisGenerator(target_size_mm=100.0)
    
    # Generate a single model
    result = generator.generate(
        prompt="a futuristic chair",
        output_path=Path("outputs/chair.stl")
    )
    
    if result["success"]:
        print(f"✓ Generated: {result['output_path']}")
        print(f"  Watertight: {result['is_watertight']}")
        print(f"  Vertices: {len(result['mesh'].vertices)}")
    else:
        print(f"✗ Failed: {result['error']}")


# =============================================================================
# Example 6: Batch Generation
# =============================================================================

def example_batch_generation():
    """
    Generate multiple models in batch.
    
    Useful for:
    - Creating variations
    - Testing different prompts
    - Building model libraries
    """
    from pathlib import Path
    from src.core.trellis_generator import TrellisGenerator
    
    # Initialize generator once
    generator = TrellisGenerator(target_size_mm=100.0)
    
    # List of prompts to generate
    prompts = [
        "a coffee mug",
        "a decorative vase",
        "a toy car",
        "a desk organizer",
        "a plant pot"
    ]
    
    # Generate each model
    for i, prompt in enumerate(prompts):
        print(f"\nGenerating {i+1}/{len(prompts)}: {prompt}")
        
        output_path = Path(f"outputs/batch_{i+1}.stl")
        result = generator.generate(prompt, output_path)
        
        if result["success"]:
            print(f"✓ Success: {output_path}")
        else:
            print(f"✗ Failed: {result['error']}")


# =============================================================================
# Example 7: Integration with Blender
# =============================================================================

"""
Complete Workflow: Gradio → Blender

1. Generate model in Gradio UI:
   - Open http://localhost:7860
   - Generate "a modern vase"
   - Download saves to outputs/modern_vase.stl

2. Import to Blender:
   - Open Blender
   - Press 'N' to open sidebar
   - Go to "NeuroForge" tab
   - Click "Refresh"
   - Select "modern_vase.stl"
   - Click "Import STL"

3. Model is now in Blender:
   - Centered at origin
   - Smooth shading applied
   - Ready for editing, materials, rendering
"""


# =============================================================================
# Example 8: Using Seed for Reproducibility
# =============================================================================

"""
Using Seeds for Reproducible Results:

In the Gradio UI:
1. Enter prompt: "a coffee mug"
2. Set seed: 42
3. Click "Generate"
4. Note the result

Later:
1. Enter same prompt: "a coffee mug"
2. Set same seed: 42
3. Click "Generate"
4. Result will be identical!

Use -1 for random seed (different result each time).
"""


# =============================================================================
# Example 9: Troubleshooting
# =============================================================================

"""
Common Issues and Solutions:

Issue: "Module 'gradio' not found"
Solution: 
    pip install -r requirements.txt
    # Or in Docker:
    docker-compose up

Issue: "Output directory doesn't exist"
Solution:
    mkdir outputs
    # Or verify Docker volume mapping

Issue: "Generation takes too long"
Solution:
    - Normal: 2-5 minutes per model
    - Use queue system (automatic in Gradio)
    - Check GPU availability

Issue: "Model is too small/large in Blender"
Solution:
    - Adjust "Target Size" in Gradio UI
    - Default: 100mm (largest dimension)
    - Or scale in Blender after import

Issue: "Cannot access UI from another computer"
Solution:
    # Launch with server_name="0.0.0.0"
    app.launch(server_name="0.0.0.0", server_port=7860)
    # Or use share=True for public URL
"""


# =============================================================================
# Example 10: Advanced - Custom Queue Settings
# =============================================================================

def example_custom_queue():
    """
    Launch UI with custom queue settings.
    
    Useful for:
    - High-traffic scenarios
    - Managing multiple concurrent users
    - Optimizing resource usage
    """
    from src.ui.app import NeuroForgeApp
    import gradio as gr
    
    app = NeuroForgeApp()
    interface = app.create_interface()
    
    # Custom queue settings
    interface.queue(
        max_size=20,                    # Maximum queue size
        default_concurrency_limit=2,    # Process 2 requests simultaneously
        api_open=True                   # Enable API access
    )
    
    interface.launch(
        server_name="0.0.0.0",
        server_port=7860
    )


if __name__ == "__main__":
    # Run basic example
    print("Starting NeuroForge 3D Gradio Interface...")
    print("Access the UI at http://localhost:7860")
    print("\nPress Ctrl+C to stop\n")
    
    example_basic_launch()
