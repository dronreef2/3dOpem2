# NeuroForge 3D Importer - Blender Add-on

A Blender add-on for importing AI-generated 3D models from NeuroForge 3D directly into your Blender scenes.

## Features

- 🔄 **Auto-refresh**: Scan and list all STL files from NeuroForge output directory
- 📦 **Smart Import**: Automatically centers imported models and applies smooth shading
- 🎨 **Easy Integration**: Simple panel in Blender's N-Panel sidebar
- ⚙️ **Configurable**: Set your output directory in add-on preferences

## Requirements

- **Blender**: Version 3.0 or higher
- **NeuroForge 3D**: Running container or access to the output directory
- **Docker Volume**: Mapped output directory (if using Docker)

## Installation

### Method 1: Direct Installation (Recommended)

1. **Open Blender**
2. Go to `Edit > Preferences > Add-ons`
3. Click `Install...` button
4. Navigate to `blender_plugin/neuroforge_importer/` directory
5. Select the `__init__.py` file
6. Click `Install Add-on`
7. Enable the add-on by checking the checkbox next to "Import-Export: NeuroForge 3D Importer"

### Method 2: ZIP Installation

1. Create a ZIP file containing the `neuroforge_importer` folder:
   ```bash
   cd blender_plugin
   zip -r neuroforge_importer.zip neuroforge_importer/
   ```

2. In Blender:
   - Go to `Edit > Preferences > Add-ons`
   - Click `Install...`
   - Select the `neuroforge_importer.zip` file
   - Enable the add-on

### Method 3: Manual Installation

1. Locate your Blender scripts directory:
   - **Windows**: `%APPDATA%\Blender Foundation\Blender\<version>\scripts\addons\`
   - **macOS**: `~/Library/Application Support/Blender/<version>/scripts/addons/`
   - **Linux**: `~/.config/blender/<version>/scripts/addons/`

2. Copy the entire `neuroforge_importer` folder to the `addons` directory

3. Restart Blender

4. Enable the add-on in `Edit > Preferences > Add-ons`

## Configuration

### Setting the Output Directory

1. Open Blender Preferences: `Edit > Preferences`
2. Go to `Add-ons` tab
3. Search for "NeuroForge"
4. Expand the add-on settings
5. Set the **Output Directory** path

#### Docker Users

If you're running NeuroForge 3D in Docker, you need to:

1. **Map the output volume** when running the container:
   ```bash
   docker run --gpus all -it --rm \
     -v $(pwd)/outputs:/app/outputs \
     -p 7860:7860 \
     neuroforge3d:sprint1
   ```

2. **Set the local path** in Blender preferences:
   - Windows: `C:\path\to\3dOpem2\outputs`
   - macOS/Linux: `/path/to/3dOpem2/outputs`

#### Using Docker Compose

The included `docker-compose.yml` already maps the volume:
```yaml
volumes:
  - ./outputs:/app/outputs
```

Simply set the output directory to your local `outputs` folder.

## Usage

### Quick Start

1. **Open the Panel**:
   - Press `N` in the 3D Viewport to open the sidebar
   - Click on the **NeuroForge** tab

2. **Verify Configuration**:
   - Check that the output directory is displayed correctly
   - If not, configure it in add-on preferences

3. **Refresh File List**:
   - Click the **Refresh File List** button
   - This scans the output directory for STL files

4. **Select and Import**:
   - Choose a file from the dropdown menu
   - Click the **Import STL** button
   - The model will be imported, centered, and smoothed automatically

### Features in Detail

#### Auto-Centering

When you import a model, the add-on automatically:
- Sets the object's origin to its geometric center
- Moves the object to the world origin (0, 0, 0)
- Makes it easy to work with multiple imported models

#### Smooth Shading

The add-on applies smooth shading automatically with:
- `Shade Smooth` operation
- Auto-smooth enabled (if available)
- 60-degree smooth angle for better edge detection

#### File Management

The dropdown list shows:
- All `.stl` files in the output directory
- Files sorted alphabetically
- Real-time refresh when you click "Refresh"

## Workflow Example

### Complete Text-to-Blender Workflow

1. **Generate Model** (in NeuroForge Gradio UI):
   ```
   Prompt: "a modern coffee mug"
   Size: 100mm
   Click "Generate"
   ```

2. **Wait for Generation**:
   - Model is saved to `outputs/modern_coffee_mug.stl`

3. **Import to Blender**:
   - Open Blender
   - Press `N` → NeuroForge tab
   - Click "Refresh"
   - Select "modern_coffee_mug.stl"
   - Click "Import STL"

4. **Work with Model**:
   - Model is now centered in your scene
   - Smooth shading is already applied
   - Ready for further editing, materials, rendering, etc.

## Troubleshooting

### "Output directory not set or doesn't exist"

**Solution**: Configure the output directory in add-on preferences.

1. `Edit > Preferences > Add-ons`
2. Find "NeuroForge 3D Importer"
3. Set the correct path to your outputs folder

### "No STL files found"

**Possible causes**:
- Output directory is empty (generate models first)
- Wrong directory path configured
- Docker volume not mapped correctly

**Solution**:
1. Verify the directory path in preferences
2. Check that STL files exist in that directory
3. For Docker users, verify volume mapping

### "File not found" after selecting a file

**Solution**: Click "Refresh" to update the file list before importing.

### Import succeeds but object not visible

**Check**:
1. Object may be very small or very large
2. Press `Numpad .` to frame the selected object
3. Check the object's scale in the properties panel

## Development

### Add-on Structure

```
neuroforge_importer/
└── __init__.py         # Main add-on file
    ├── bl_info         # Add-on metadata
    ├── Preferences     # Configuration UI
    ├── Operators       # Import and refresh operations
    ├── Panel           # UI panel in sidebar
    └── Properties      # Scene properties for file selection
```

### Customization

To modify the add-on behavior, edit `__init__.py`:

- **Change smooth angle**: Edit `auto_smooth_angle` in `NEUROFORGE_OT_ImportSTL`
- **Add post-import operations**: Add code after the import operation
- **Modify UI**: Edit `NEUROFORGE_PT_MainPanel.draw()`

## Compatibility

### Tested Blender Versions

- ✅ Blender 3.0
- ✅ Blender 3.1
- ✅ Blender 3.2+
- ✅ Blender 4.0+

### Platform Support

- ✅ Windows 10/11
- ✅ macOS (Intel and Apple Silicon)
- ✅ Linux (Ubuntu, Fedora, etc.)

## Support

For issues, questions, or contributions:

- **GitHub Issues**: [dronreef2/3dOpem2/issues](https://github.com/dronreef2/3dOpem2/issues)
- **Documentation**: Main project README

## License

This add-on is part of the NeuroForge 3D project and is licensed under the MIT License.

## Credits

- **NeuroForge 3D Team**
- Based on [Microsoft TRELLIS](https://github.com/microsoft/TRELLIS)

---

**Happy 3D Modeling!** 🎨
