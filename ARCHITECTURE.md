# NeuroForge 3D Architecture - Sprint 4

## System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     NeuroForge 3D System                     │
└─────────────────────────────────────────────────────────────┘

┌──────────────────────┐         ┌──────────────────────┐
│   Web Interface      │         │   Blender Plugin     │
│   (Gradio UI)        │         │   (N-Panel Add-on)   │
└──────────────────────┘         └──────────────────────┘
         │                                  │
         │ HTTP (port 7860)                │ File System
         │                                  │
         ▼                                  ▼
┌──────────────────────────────────────────────────────────────┐
│                      Docker Container                         │
│  ┌────────────────────────────────────────────────────────┐  │
│  │              TrellisGenerator (Core)                   │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │  │
│  │  │ Text-to-Image│→ │  Background  │→ │ Image-to-3D  │ │  │
│  │  │ (SDXL/SD1.5) │  │   Removal    │  │  (TRELLIS)   │ │  │
│  │  │              │  │   (rembg)    │  │              │ │  │
│  │  └──────────────┘  └──────────────┘  └──────────────┘ │  │
│  │                           │                            │  │
│  │                           ▼                            │  │
│  │              ┌────────────────────────┐               │  │
│  │              │ Processing Pipeline    │               │  │
│  │              │ - Mesh Repair          │               │  │
│  │              │ - Scaling              │               │  │
│  │              │ - Validation           │               │  │
│  │              └────────────────────────┘               │  │
│  └────────────────────────────────────────────────────────┘  │
│                           │                                   │
│                           ▼                                   │
│              ┌────────────────────────┐                       │
│              │   outputs/             │ ◄──── Volume Mount   │
│              │   ├── model1.stl       │                       │
│              │   ├── model2.stl       │                       │
│              │   └── ...              │                       │
│              └────────────────────────┘                       │
└──────────────────────────────────────────────────────────────┘
```

## Component Details

### 1. Web Interface (Gradio)

**File:** `src/ui/app.py`

```
NeuroForgeApp
│
├─ Inputs
│  ├─ Text Prompt: "a modern coffee mug"
│  ├─ Target Size: 100mm
│  └─ Seed: 42 (optional)
│
├─ Processing
│  ├─ Validate inputs
│  ├─ Initialize TrellisGenerator
│  ├─ Generate 3D model
│  └─ Track progress
│
└─ Outputs
   ├─ 3D Viewer (gr.Model3D)
   ├─ Download Button (gr.File)
   └─ Status Message
```

**Features:**
- 🌐 Web-based, no installation needed
- 🎨 Interactive 3D preview
- ⏳ Queue system for long requests
- 📥 Direct STL download
- 🔄 Real-time progress tracking

### 2. Blender Plugin

**File:** `blender_plugin/neuroforge_importer/__init__.py`

```
Blender Add-on
│
├─ Preferences
│  └─ Output Directory: /path/to/outputs
│
├─ N-Panel UI
│  ├─ Refresh Button
│  │  └─ Scans directory for .stl files
│  │
│  ├─ File Dropdown
│  │  └─ Lists available models
│  │
│  └─ Import Button
│     ├─ Import STL
│     ├─ Center at origin
│     └─ Apply smooth shading
│
└─ Operators
   ├─ NEUROFORGE_OT_RefreshFiles
   └─ NEUROFORGE_OT_ImportSTL
```

**Features:**
- 🔌 One-click installation
- 🔄 Auto-scan output directory
- 📦 Smart import with processing
- 🎯 Auto-centering
- ✨ Auto-smooth shading

### 3. Core Pipeline

**Flow:**

```
User Input
    ↓
┌─────────────────────┐
│ Text Prompt         │  "a futuristic chair"
└─────────────────────┘
    ↓
┌─────────────────────┐
│ SDXL-Turbo          │  Generate 2D image
│ (Text-to-Image)     │  ~4 inference steps
└─────────────────────┘
    ↓
┌─────────────────────┐
│ rembg               │  Remove background
│ (Background Removal)│  Create transparency
└─────────────────────┘
    ↓
┌─────────────────────┐
│ TRELLIS             │  Convert to 3D mesh
│ (Image-to-3D)       │  Generate geometry
└─────────────────────┘
    ↓
┌─────────────────────┐
│ Mesh Repair         │  Fix topology
│ (PyMeshFix)         │  Fill holes
└─────────────────────┘
    ↓
┌─────────────────────┐
│ Mesh Scaling        │  Normalize size
│ (Target: 100mm)     │  Preserve ratio
└─────────────────────┘
    ↓
┌─────────────────────┐
│ Validation          │  Check watertight
│ (mesh.is_watertight)│  Verify printability
└─────────────────────┘
    ↓
┌─────────────────────┐
│ Save STL            │  outputs/model.stl
└─────────────────────┘
    ↓
Ready for 3D Printing! 🎉
```

## User Workflows

### Workflow A: Web-Only

```
1. User → Opens http://localhost:7860
         ↓
2. User → Enters prompt: "a decorative vase"
         ↓
3. User → Sets size: 100mm
         ↓
4. User → Clicks "Generate"
         ↓
5. System → Generates model (2-5 min)
         ↓
6. User → Views 3D model in browser
         ↓
7. User → Downloads STL file
         ↓
8. User → 3D prints the model 🎉
```

### Workflow B: Web + Blender

```
1. User → Generates model in Gradio UI
         ↓
         Saves to: outputs/decorative_vase.stl
         ↓
2. User → Opens Blender
         ↓
3. User → Press 'N' → NeuroForge tab
         ↓
4. User → Clicks "Refresh"
         ↓
         Plugin scans outputs/ directory
         ↓
5. User → Selects "decorative_vase.stl"
         ↓
6. User → Clicks "Import STL"
         ↓
         Plugin imports, centers, smooths
         ↓
7. User → Edits, adds materials, renders
         ↓
8. User → Exports or 3D prints 🎉
```

### Workflow C: Batch Generation

```
1. Developer → Uses programmatic API
              ↓
2. Script → Generates multiple models
           ├─ coffee_mug.stl
           ├─ vase.stl
           ├─ toy_car.stl
           └─ ...
              ↓
3. User → Opens Blender
         ↓
4. User → Imports all models
         ↓
5. User → Creates scene with all objects 🎉
```

## Technology Stack

### Frontend (UI)
- **Gradio 5.11.0**: Web interface framework
- **gr.Model3D**: 3D model viewer component
- **gr.File**: File download component

### Backend (Core)
- **TrellisGenerator**: Main generation class
- **Stable Diffusion**: Text-to-image (SDXL-Turbo)
- **rembg**: Background removal
- **TRELLIS**: Image-to-3D conversion

### Processing
- **Trimesh**: Mesh operations
- **PyMeshFix**: Mesh repair
- **NumPy**: Numerical operations

### Blender Integration
- **bpy**: Blender Python API
- **Blender 3.0+**: 3D software

### Infrastructure
- **Docker**: Containerization
- **CUDA 12.1**: GPU acceleration
- **PyTorch 2.4.0**: Deep learning framework

## File Structure

```
3dOpem2/
│
├── src/
│   ├── ui/
│   │   ├── __init__.py
│   │   └── app.py                   # Gradio web interface
│   │
│   ├── core/
│   │   ├── base_generator.py
│   │   ├── mock_generator.py
│   │   └── trellis_generator.py    # Main AI generator
│   │
│   └── processing/
│       ├── mesh_repair.py
│       ├── mesh_scaling.py
│       ├── mesh_validator.py
│       └── pipeline.py
│
├── blender_plugin/
│   ├── README.md                    # Installation guide
│   └── neuroforge_importer/
│       └── __init__.py              # Blender add-on
│
├── tests/
│   ├── test_ui.py                   # UI tests
│   ├── test_trellis_generator.py
│   └── test_processing.py
│
├── outputs/                          # Generated STL files
│
├── launch_ui.py                      # UI launcher
├── examples_ui.py                    # Usage examples
├── docker-compose.yml                # Docker config
└── README.md                         # Main docs
```

## Deployment Options

### Option 1: Docker Compose (Recommended)

```bash
docker-compose up
# Access: http://localhost:7860
# Outputs: ./outputs/
```

### Option 2: Docker Run

```bash
docker run --gpus all -p 7860:7860 \
  -v $(pwd)/outputs:/app/outputs \
  neuroforge3d:latest python launch_ui.py
```

### Option 3: Local Development

```bash
python launch_ui.py
# Requires: Python 3.10+, CUDA 12.1, dependencies
```

## Performance Characteristics

### Generation Time
- **Text-to-Image**: ~10-30 seconds (SDXL-Turbo)
- **Background Removal**: ~5-10 seconds (rembg)
- **Image-to-3D**: ~1-3 minutes (TRELLIS)
- **Processing**: ~5-15 seconds (repair + scale)
- **Total**: ~2-5 minutes per model

### Resource Requirements
- **VRAM**: 8GB+ recommended (4GB minimum with CPU offload)
- **RAM**: 16GB+ recommended
- **Disk**: ~10GB for models + outputs
- **CPU**: Multi-core recommended

### Scalability
- **Queue System**: Handles multiple concurrent requests
- **Batch Processing**: Supported via API
- **GPU Sharing**: One model at a time (serialized)

## Security

- ✅ **CodeQL**: 0 vulnerabilities detected
- ✅ **Input Validation**: All user inputs validated
- ✅ **Path Sanitization**: Safe filename generation
- ✅ **Error Handling**: No sensitive info in errors
- ✅ **Docker Isolation**: Runs in container

## Future Enhancements

1. **UI Improvements**
   - Model gallery
   - History/favorites
   - Advanced parameters
   - Multi-model comparison

2. **Blender Extensions**
   - Material presets
   - Auto-UV unwrapping
   - Batch import
   - Scene templates

3. **Performance**
   - Model caching
   - Parallel generation
   - GPU optimization
   - Queue prioritization

4. **Integration**
   - REST API
   - CLI tool
   - Python package
   - CI/CD pipelines

---

**Architecture Version:** Sprint 4  
**Last Updated:** 2025-11-21  
**Status:** Production Ready ✅
