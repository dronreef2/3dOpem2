"""
NeuroForge 3D Importer - Blender Add-on

This add-on provides a convenient interface for importing 3D models generated
by NeuroForge 3D directly into Blender.

Features:
- Browse and list STL files from the NeuroForge output directory
- Import selected STL files with automatic centering
- Apply smooth shading automatically
- Configure the output directory path

Installation:
1. Open Blender
2. Go to Edit > Preferences > Add-ons
3. Click "Install" and select this __init__.py file (or the zip containing it)
4. Enable the "Import-Export: NeuroForge 3D Importer" add-on
5. Configure the output directory path in the add-on preferences

Usage:
1. Press 'N' in the 3D Viewport to open the sidebar
2. Find the "NeuroForge" tab
3. Set the output directory (where Docker saves STL files)
4. Click "Refresh" to list available STL files
5. Select a file from the dropdown
6. Click "Import STL" to bring it into your scene

Requirements:
- Blender 3.0 or higher
- NeuroForge 3D container running (or access to output directory)
"""

bl_info = {
    "name": "NeuroForge 3D Importer",
    "author": "NeuroForge 3D Team",
    "version": (1, 0, 0),
    "blender": (3, 0, 0),
    "location": "View3D > Sidebar > NeuroForge",
    "description": "Import AI-generated 3D models from NeuroForge 3D",
    "warning": "",
    "doc_url": "https://github.com/dronreef2/3dOpem2",
    "category": "Import-Export",
}

import bpy
from bpy.props import StringProperty, EnumProperty
from bpy.types import Operator, Panel, AddonPreferences
from pathlib import Path
import os


# ============================================================================
# Add-on Preferences
# ============================================================================

class NeuroForgePreferences(AddonPreferences):
    """
    Preferences for NeuroForge 3D Importer add-on.
    
    Allows users to configure the output directory where NeuroForge
    saves generated STL files.
    """
    bl_idname = __name__

    output_directory: StringProperty(
        name="Output Directory",
        description="Path to the NeuroForge outputs directory (where STL files are saved)",
        default="",
        subtype='DIR_PATH'
    )

    def draw(self, context):
        """Draw the preferences UI."""
        layout = self.layout
        layout.label(text="NeuroForge 3D Configuration")
        layout.prop(self, "output_directory")
        
        # Show a helpful message
        box = layout.box()
        box.label(text="Docker Volume Mapping:", icon='INFO')
        box.label(text="If using Docker, map the container's /app/outputs to a local folder.")
        box.label(text="Example: -v ./outputs:/app/outputs")


# ============================================================================
# Operators
# ============================================================================

class NEUROFORGE_OT_RefreshFiles(Operator):
    """Refresh the list of available STL files"""
    bl_idname = "neuroforge.refresh_files"
    bl_label = "Refresh File List"
    bl_description = "Scan the output directory for STL files"
    bl_options = {'REGISTER'}

    def execute(self, context):
        """Execute the refresh operation."""
        scene = context.scene
        prefs = context.preferences.addons[__name__].preferences
        
        # Get output directory from preferences
        output_dir = prefs.output_directory
        
        if not output_dir or not os.path.exists(output_dir):
            self.report({'WARNING'}, "Output directory not set or doesn't exist. Check add-on preferences.")
            return {'CANCELLED'}
        
        # Scan for STL files
        try:
            output_path = Path(output_dir)
            stl_files = sorted(output_path.glob("*.stl"))
            
            if not stl_files:
                self.report({'INFO'}, f"No STL files found in {output_dir}")
                return {'FINISHED'}
            
            # Store file list in scene property
            # We'll use this to populate the dropdown
            scene.neuroforge_file_count = len(stl_files)
            
            self.report({'INFO'}, f"Found {len(stl_files)} STL file(s)")
            return {'FINISHED'}
            
        except Exception as e:
            self.report({'ERROR'}, f"Error scanning directory: {str(e)}")
            return {'CANCELLED'}


class NEUROFORGE_OT_ImportSTL(Operator):
    """Import the selected STL file into Blender"""
    bl_idname = "neuroforge.import_stl"
    bl_label = "Import STL"
    bl_description = "Import the selected STL file, center it, and apply smooth shading"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        """Execute the import operation."""
        scene = context.scene
        prefs = context.preferences.addons[__name__].preferences
        
        # Get output directory
        output_dir = prefs.output_directory
        if not output_dir or not os.path.exists(output_dir):
            self.report({'WARNING'}, "Output directory not set or doesn't exist")
            return {'CANCELLED'}
        
        # Get selected file
        selected_file = scene.neuroforge_selected_file
        if not selected_file:
            self.report({'WARNING'}, "No file selected")
            return {'CANCELLED'}
        
        # Construct full path
        file_path = os.path.join(output_dir, selected_file)
        if not os.path.exists(file_path):
            self.report({'ERROR'}, f"File not found: {file_path}")
            return {'CANCELLED'}
        
        try:
            # Import the STL file
            bpy.ops.import_mesh.stl(filepath=file_path)
            
            # Get the imported object (should be the active object)
            imported_obj = context.active_object
            
            if imported_obj is None:
                self.report({'WARNING'}, "Import succeeded but no object was created")
                return {'FINISHED'}
            
            # Center the object at the origin
            # First, ensure we're in object mode
            if imported_obj.mode != 'OBJECT':
                bpy.ops.object.mode_set(mode='OBJECT')
            
            # Set origin to geometry center
            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
            
            # Move to world origin
            imported_obj.location = (0, 0, 0)
            
            # Apply smooth shading
            # Select only this object
            bpy.ops.object.select_all(action='DESELECT')
            imported_obj.select_set(True)
            context.view_layer.objects.active = imported_obj
            
            # Apply smooth shading
            bpy.ops.object.shade_smooth()
            
            # Optional: Set smooth angle (Auto Smooth)
            # This helps with edge detection for smooth shading
            # Note: use_auto_smooth is deprecated in Blender 4.1+
            # For newer versions, smooth shading is sufficient
            try:
                if hasattr(imported_obj.data, "use_auto_smooth"):
                    imported_obj.data.use_auto_smooth = True
                    imported_obj.data.auto_smooth_angle = 1.0472  # ~60 degrees in radians
            except AttributeError:
                # Blender 4.1+ - auto smooth is handled differently
                # Shade smooth is sufficient for most cases
                pass
            
            self.report({'INFO'}, f"Successfully imported: {selected_file}")
            return {'FINISHED'}
            
        except Exception as e:
            self.report({'ERROR'}, f"Import failed: {str(e)}")
            return {'CANCELLED'}


# ============================================================================
# UI Panel
# ============================================================================

class NEUROFORGE_PT_MainPanel(Panel):
    """Main panel for NeuroForge 3D Importer"""
    bl_label = "NeuroForge 3D"
    bl_idname = "NEUROFORGE_PT_main_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'NeuroForge'

    def draw(self, context):
        """Draw the panel UI."""
        layout = self.layout
        scene = context.scene
        prefs = context.preferences.addons[__name__].preferences
        
        # Header
        box = layout.box()
        box.label(text="🎨 NeuroForge 3D Importer", icon='MESH_CUBE')
        
        # Configuration section
        layout.separator()
        layout.label(text="Configuration:", icon='PREFERENCES')
        
        # Output directory display
        col = layout.column(align=True)
        if prefs.output_directory:
            col.label(text="Output Dir:", icon='FILE_FOLDER')
            
            # Split long paths for display
            dir_path = prefs.output_directory
            if len(dir_path) > 30:
                col.label(text=f"...{dir_path[-27:]}")
            else:
                col.label(text=dir_path)
        else:
            col.label(text="⚠️ Output directory not set!", icon='ERROR')
            col.label(text="Configure in add-on preferences.")
        
        # Refresh button
        layout.separator()
        row = layout.row()
        row.scale_y = 1.5
        row.operator("neuroforge.refresh_files", icon='FILE_REFRESH')
        
        # File selection
        layout.separator()
        layout.label(text="Available Files:", icon='FILE_3D')
        
        # Get list of files
        output_dir = prefs.output_directory
        if output_dir and os.path.exists(output_dir):
            output_path = Path(output_dir)
            stl_files = sorted(output_path.glob("*.stl"))
            
            if stl_files:
                # Create items for enum property
                items = [(f.name, f.name, f"Import {f.name}") for f in stl_files]
                
                # Update the enum property dynamically
                # Note: This is a simplified approach. For production,
                # consider using a CollectionProperty for better performance
                
                # File dropdown
                col = layout.column(align=True)
                col.prop(scene, "neuroforge_selected_file", text="")
                
                # Import button
                row = layout.row()
                row.scale_y = 2.0
                row.operator("neuroforge.import_stl", icon='IMPORT')
                
                # File info
                layout.separator()
                box = layout.box()
                box.label(text=f"Files found: {len(stl_files)}", icon='INFO')
            else:
                layout.label(text="No STL files found", icon='INFO')
                layout.label(text="Generate models in NeuroForge first")
        else:
            layout.label(text="Invalid output directory", icon='ERROR')
        
        # Help section
        layout.separator()
        box = layout.box()
        box.label(text="Quick Start:", icon='HELP')
        col = box.column(align=True)
        col.label(text="1. Set output directory in preferences")
        col.label(text="2. Click 'Refresh' to scan for files")
        col.label(text="3. Select a file from the dropdown")
        col.label(text="4. Click 'Import STL'")


# ============================================================================
# Property Definitions
# ============================================================================

def get_stl_files(self, context):
    """
    Get list of STL files for the enum property.
    
    This is called by Blender to populate the dropdown.
    """
    prefs = context.preferences.addons[__name__].preferences
    output_dir = prefs.output_directory
    
    if not output_dir or not os.path.exists(output_dir):
        return [("NONE", "No directory set", "Configure output directory in preferences")]
    
    try:
        output_path = Path(output_dir)
        stl_files = sorted(output_path.glob("*.stl"))
        
        if not stl_files:
            return [("NONE", "No STL files", "No STL files found in output directory")]
        
        items = [(f.name, f.name, f"Import {f.name}") for f in stl_files]
        return items
        
    except Exception as e:
        return [("ERROR", f"Error: {str(e)}", "Error scanning directory")]


# ============================================================================
# Registration
# ============================================================================

classes = (
    NeuroForgePreferences,
    NEUROFORGE_OT_RefreshFiles,
    NEUROFORGE_OT_ImportSTL,
    NEUROFORGE_PT_MainPanel,
)


def register():
    """Register the add-on."""
    for cls in classes:
        bpy.utils.register_class(cls)
    
    # Register scene properties
    bpy.types.Scene.neuroforge_selected_file = EnumProperty(
        name="STL File",
        description="Select an STL file to import",
        items=get_stl_files
    )
    
    bpy.types.Scene.neuroforge_file_count = bpy.props.IntProperty(
        name="File Count",
        default=0
    )


def unregister():
    """Unregister the add-on."""
    # Unregister scene properties
    del bpy.types.Scene.neuroforge_selected_file
    del bpy.types.Scene.neuroforge_file_count
    
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
