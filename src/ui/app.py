#!/usr/bin/env python3
"""
Gradio Web Interface for NeuroForge 3D.

This module provides a user-friendly web interface for generating 3D models
from text prompts using the TrellisGenerator. It allows users to:
- Enter text prompts describing the desired 3D object
- Configure generation parameters (size, seed)
- Visualize the generated 3D model interactively
- Download the resulting STL file for 3D printing

The interface uses Gradio 5.11.0 for the web UI and includes queue management
for handling long-running generation requests without timeout.
"""

import logging
from pathlib import Path
from typing import Optional, Tuple
import gradio as gr

from ..core.trellis_generator import TrellisGenerator

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Output directory for generated models
OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)


class NeuroForgeApp:
    """
    Gradio application for NeuroForge 3D text-to-3D generation.
    
    This class encapsulates the Gradio interface and manages the
    TrellisGenerator instance for generating 3D models.
    
    Attributes:
        generator: TrellisGenerator instance for creating 3D models
        
    Example:
        >>> app = NeuroForgeApp()
        >>> app.launch()
    """
    
    def __init__(self):
        """Initialize the NeuroForge Gradio application."""
        logger.info("Initializing NeuroForge 3D Gradio App")
        self.generator: Optional[TrellisGenerator] = None
        
    def _initialize_generator(
        self,
        target_size_mm: float = 100.0
    ) -> None:
        """
        Lazy initialization of TrellisGenerator.
        
        This delays model loading until the first generation request,
        avoiding long startup times.
        
        Args:
            target_size_mm: Target size for generated meshes in millimeters.
        """
        if self.generator is None:
            logger.info(f"Loading TrellisGenerator (target size: {target_size_mm}mm)")
            try:
                self.generator = TrellisGenerator(target_size_mm=target_size_mm)
                logger.info("TrellisGenerator loaded successfully")
            except Exception as e:
                logger.error(f"Failed to load TrellisGenerator: {e}", exc_info=True)
                raise
    
    def generate_3d_model(
        self,
        prompt: str,
        target_size_mm: float,
        seed: Optional[int] = None,
        progress: gr.Progress = gr.Progress()
    ) -> Tuple[Optional[str], Optional[str], str]:
        """
        Generate a 3D model from a text prompt.
        
        This is the main generation function called by the Gradio interface.
        It manages the complete pipeline from text to STL file.
        
        Args:
            prompt: Text description of the 3D object to generate.
            target_size_mm: Target size of the largest dimension in millimeters.
            seed: Optional random seed for reproducibility. If None, uses random.
            progress: Gradio progress tracker for UI updates.
            
        Returns:
            Tuple containing:
                - Path to generated STL file (for Model3D viewer)
                - Path to generated STL file (for File download)
                - Status message describing the result
                
        Note:
            Returns (None, None, error_message) if generation fails.
        """
        # Validate inputs
        if not prompt or len(prompt.strip()) == 0:
            error_msg = "⚠️ Please enter a text prompt describing the 3D model."
            logger.warning("Empty prompt provided")
            return None, None, error_msg
        
        if target_size_mm <= 0 or target_size_mm > 500:
            error_msg = "⚠️ Target size must be between 1mm and 500mm."
            logger.warning(f"Invalid target size: {target_size_mm}mm")
            return None, None, error_msg
        
        try:
            # Update progress
            progress(0.1, desc="Initializing model...")
            
            # Initialize generator if needed
            self._initialize_generator(target_size_mm)
            
            # Set seed if provided
            if seed is not None and seed >= 0:
                import torch
                import random
                import numpy as np
                
                torch.manual_seed(seed)
                random.seed(seed)
                np.random.seed(seed)
                logger.info(f"Random seed set to: {seed}")
            
            # Generate output filename
            import re
            safe_prompt = re.sub(r'[^\w\s-]', '', prompt.lower())[:30]
            safe_prompt = re.sub(r'[-\s]+', '_', safe_prompt)
            output_filename = f"{safe_prompt}.stl"
            output_path = OUTPUT_DIR / output_filename
            
            logger.info(f"Starting generation for prompt: '{prompt}'")
            logger.info(f"Target size: {target_size_mm}mm, Output: {output_path}")
            
            # Update progress
            progress(0.2, desc="Generating 2D image from text...")
            
            # Generate 3D model
            result = self.generator.generate(prompt, output_path)
            
            # Update progress
            progress(1.0, desc="Generation complete!")
            
            if result["success"]:
                # Success!
                stats = result.get("pipeline_stats", {})
                vertices = len(result["mesh"].vertices)
                faces = len(result["mesh"].faces)
                volume = stats.get("volume_mm3", 0)
                
                success_msg = f"""✅ **Generation Successful!**

📝 Prompt: {prompt}
📏 Target Size: {target_size_mm}mm
🔺 Vertices: {vertices:,}
🔶 Faces: {faces:,}
📦 Volume: {volume:.2f} mm³
✓ Watertight: {result['is_watertight']}

📥 Ready to download!
"""
                logger.info(f"Successfully generated: {output_path}")
                
                # Return paths for both Model3D viewer and File download
                return str(output_path), str(output_path), success_msg
            else:
                # Generation failed
                error = result.get("error", "Unknown error")
                error_msg = f"""❌ **Generation Failed**

Error: {error}

Please try:
- Simplifying your prompt
- Using a different random seed
- Checking the logs for details
"""
                logger.error(f"Generation failed: {error}")
                return None, None, error_msg
                
        except Exception as e:
            error_msg = f"""❌ **Unexpected Error**

{str(e)}

Please check the console logs for more details.
"""
            logger.error(f"Unexpected error during generation: {e}", exc_info=True)
            return None, None, error_msg
    
    def create_interface(self) -> gr.Blocks:
        """
        Create the Gradio interface.
        
        Returns:
            Gradio Blocks interface ready to launch.
        """
        with gr.Blocks(
            title="NeuroForge 3D - Text to 3D Model Generator",
            theme=gr.themes.Soft()
        ) as interface:
            gr.Markdown("""
# 🎨 NeuroForge 3D - Text-to-3D Generator

Generate printable 3D models from text descriptions using AI.

Powered by Microsoft TRELLIS and optimized for 3D printing (watertight STL files).
""")
            
            with gr.Row():
                with gr.Column(scale=1):
                    gr.Markdown("### 📝 Input")
                    
                    # Text prompt input
                    prompt_input = gr.Textbox(
                        label="Describe your 3D model",
                        placeholder="Example: a futuristic chair, a decorative vase, a toy robot...",
                        lines=3,
                        max_lines=5
                    )
                    
                    # Target size slider
                    size_input = gr.Slider(
                        minimum=10,
                        maximum=500,
                        value=100,
                        step=10,
                        label="Target Size (mm)",
                        info="Largest dimension of the final model"
                    )
                    
                    # Seed input (optional)
                    seed_input = gr.Number(
                        label="Random Seed (optional)",
                        value=-1,
                        precision=0,
                        info="Set to -1 for random, or use a specific number for reproducibility"
                    )
                    
                    # Generate button
                    generate_btn = gr.Button(
                        "🚀 Generate 3D Model",
                        variant="primary",
                        size="lg"
                    )
                    
                    gr.Markdown("""
---
**Tips:**
- Be specific in your description
- Simple objects work best
- Generation takes 2-5 minutes
- Use seed for reproducible results
""")
                
                with gr.Column(scale=2):
                    gr.Markdown("### 🎯 Output")
                    
                    # Status message
                    status_output = gr.Markdown(
                        value="👆 Enter a prompt and click 'Generate' to start.",
                        label="Status"
                    )
                    
                    # 3D model viewer
                    model_output = gr.Model3D(
                        label="3D Preview",
                        height=400,
                        interactive=False
                    )
                    
                    # Download button
                    file_output = gr.File(
                        label="Download STL",
                        file_count="single",
                        type="filepath"
                    )
            
            # Examples
            gr.Markdown("### 💡 Example Prompts")
            gr.Examples(
                examples=[
                    ["a modern coffee mug with a curved handle", 80, -1],
                    ["a small decorative vase with geometric patterns", 100, -1],
                    ["a simple toy car", 60, -1],
                    ["a desk organizer with multiple compartments", 120, -1],
                    ["a minimalist plant pot", 90, -1]
                ],
                inputs=[prompt_input, size_input, seed_input],
                label="Click an example to try it"
            )
            
            # Connect the generate button to the function
            generate_btn.click(
                fn=self.generate_3d_model,
                inputs=[prompt_input, size_input, seed_input],
                outputs=[model_output, file_output, status_output],
                show_progress=True
            )
            
            # Footer
            gr.Markdown("""
---
**NeuroForge 3D** - Open Source Text-to-3D Pipeline  
Based on [Microsoft TRELLIS](https://github.com/microsoft/TRELLIS) | Optimized for 3D Printing
""")
        
        return interface
    
    def launch(self, **kwargs) -> None:
        """
        Launch the Gradio interface.
        
        Args:
            **kwargs: Additional arguments to pass to gr.Blocks.launch()
                     (e.g., share=True for public URL, server_name, server_port)
                     
        Example:
            >>> app = NeuroForgeApp()
            >>> app.launch(server_name="0.0.0.0", server_port=7860)
        """
        interface = self.create_interface()
        
        # Enable queueing for long-running requests
        # This prevents timeouts during model generation
        interface.queue(
            max_size=10,  # Maximum queue size
            default_concurrency_limit=1  # Process one at a time
        )
        
        logger.info("Launching Gradio interface...")
        interface.launch(**kwargs)


def main():
    """Main entry point for the Gradio app."""
    app = NeuroForgeApp()
    
    # Launch with default settings
    # In Docker, use server_name="0.0.0.0" to accept external connections
    app.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,  # Set to True for public Gradio URL
        show_error=True
    )


if __name__ == "__main__":
    main()
