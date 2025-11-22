#!/usr/bin/env python3
"""
NeuroForge 3D - Project Validation and Analysis Script

This script analyzes the project structure and validates that all
components are properly organized and functional.
"""

import os
import sys
from pathlib import Path
from typing import List, Tuple, Dict

# Color codes for terminal output
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_section(title: str):
    """Print a section header."""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{title}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}\n")

def print_success(message: str):
    """Print success message."""
    print(f"{Colors.GREEN}✓{Colors.END} {message}")

def print_warning(message: str):
    """Print warning message."""
    print(f"{Colors.YELLOW}⚠{Colors.END} {message}")

def print_error(message: str):
    """Print error message."""
    print(f"{Colors.RED}✗{Colors.END} {message}")

def print_info(message: str):
    """Print info message."""
    print(f"{Colors.BLUE}ℹ{Colors.END} {message}")

def check_directory_structure() -> Tuple[bool, List[str]]:
    """Check if all required directories exist."""
    print_section("1. Directory Structure Validation")
    
    required_dirs = [
        "src",
        "src/core",
        "src/processing",
        "src/ui",
        "src/utils",
        "tests",
        "blender_plugin",
        "blender_plugin/neuroforge_importer",
    ]
    
    optional_dirs = [
        "outputs",
        "models",
        "logs",
        "tmp",
    ]
    
    all_ok = True
    messages = []
    
    for dir_path in required_dirs:
        if Path(dir_path).is_dir():
            print_success(f"Required directory exists: {dir_path}/")
        else:
            print_error(f"Missing required directory: {dir_path}/")
            all_ok = False
            messages.append(f"Create directory: mkdir -p {dir_path}")
    
    for dir_path in optional_dirs:
        if Path(dir_path).is_dir():
            print_success(f"Optional directory exists: {dir_path}/")
        else:
            print_warning(f"Optional directory missing: {dir_path}/ (will be auto-created)")
    
    return all_ok, messages

def check_required_files() -> Tuple[bool, List[str]]:
    """Check if all required files exist."""
    print_section("2. Required Files Validation")
    
    required_files = {
        "Core Python Files": [
            "src/__init__.py",
            "src/core/__init__.py",
            "src/core/base_generator.py",
            "src/core/mock_generator.py",
            "src/core/trellis_generator.py",
            "src/processing/__init__.py",
            "src/processing/pipeline.py",
            "src/processing/mesh_repair.py",
            "src/processing/mesh_scaling.py",
            "src/processing/mesh_validator.py",
            "src/ui/__init__.py",
            "src/ui/app.py",
            "src/utils/__init__.py",
        ],
        "Test Files": [
            "tests/__init__.py",
            "tests/test_mock_generator.py",
            "tests/test_processing.py",
            "tests/test_trellis_generator.py",
            "tests/test_ui.py",
        ],
        "Scripts and Tools": [
            "demo.py",
            "launch_ui.py",
            "examples_ui.py",
            "setup.sh",
            "validate_docker.sh",
        ],
        "Docker Files": [
            "Dockerfile",
            "docker-compose.yml",
            ".dockerignore",
        ],
        "Configuration": [
            "requirements.txt",
            ".gitignore",
        ],
        "Documentation": [
            "README.md",
            "QUICK_START.md",
            "PROJECT_ORGANIZATION.md",
            "ARCHITECTURE.md",
            "TECHNICAL_BLUEPRINT.md",
            "CODING_STANDARDS.md",
            "ROADMAP.md",
            "PROJECT_CONTEXT.md",
            "blender_plugin/README.md",
        ],
        "Blender Plugin": [
            "blender_plugin/neuroforge_importer/__init__.py",
        ],
    }
    
    all_ok = True
    messages = []
    
    for category, files in required_files.items():
        print(f"\n{Colors.BOLD}{category}:{Colors.END}")
        for file_path in files:
            if Path(file_path).is_file():
                print_success(f"{file_path}")
            else:
                print_error(f"{file_path} - MISSING!")
                all_ok = False
                messages.append(f"Missing file: {file_path}")
    
    return all_ok, messages

def check_python_syntax() -> Tuple[bool, List[str]]:
    """Check Python files for syntax errors."""
    print_section("3. Python Syntax Validation")
    
    python_files = []
    for root, dirs, files in os.walk("src"):
        for file in files:
            if file.endswith(".py"):
                python_files.append(Path(root) / file)
    
    # Add other Python files
    for file in ["demo.py", "launch_ui.py", "examples_ui.py", "validate_project.py"]:
        if Path(file).exists():
            python_files.append(Path(file))
    
    all_ok = True
    messages = []
    
    for py_file in python_files:
        try:
            with open(py_file, 'r', encoding='utf-8') as f:
                compile(f.read(), py_file, 'exec')
            print_success(f"Syntax OK: {py_file}")
        except SyntaxError as e:
            print_error(f"Syntax error in {py_file}: {e}")
            all_ok = False
            messages.append(f"Fix syntax in {py_file}: {e}")
        except Exception as e:
            print_warning(f"Could not validate {py_file}: {e}")
    
    return all_ok, messages

def check_imports() -> Tuple[bool, List[str]]:
    """Check if basic imports work."""
    print_section("4. Import Validation")
    
    messages = []
    all_ok = True
    
    # Add src to path
    sys.path.insert(0, str(Path(__file__).parent / "src"))
    
    test_imports = [
        ("src.core.base_generator", "BaseGenerator"),
        ("src.core.mock_generator", "MockGenerator"),
        ("src.processing.pipeline", "ProcessingPipeline"),
        ("src.ui.app", "NeuroForgeApp"),
    ]
    
    for module_name, class_name in test_imports:
        try:
            module = __import__(module_name, fromlist=[class_name])
            getattr(module, class_name)
            print_success(f"Import OK: from {module_name} import {class_name}")
        except ImportError as e:
            print_error(f"Import failed: {module_name} - {e}")
            all_ok = False
            messages.append(f"Install dependencies: pip install -r requirements.txt")
        except AttributeError as e:
            print_error(f"Class not found: {class_name} in {module_name}")
            all_ok = False
            messages.append(f"Check implementation of {class_name}")
        except Exception as e:
            print_warning(f"Could not import {module_name}: {e}")
            if "trimesh" in str(e) or "torch" in str(e):
                messages.append("Install dependencies: pip install trimesh scipy numpy")
    
    return all_ok, messages

def check_documentation() -> Tuple[bool, List[str]]:
    """Check documentation completeness."""
    print_section("5. Documentation Validation")
    
    required_docs = {
        "README.md": ["Quick Start", "Installation", "Usage"],
        "QUICK_START.md": ["Docker", "Blender", "Web Interface"],
        "PROJECT_ORGANIZATION.md": ["Estrutura", "Componentes", "Fluxo"],
    }
    
    all_ok = True
    messages = []
    
    for doc_file, required_sections in required_docs.items():
        if not Path(doc_file).exists():
            print_error(f"{doc_file} - MISSING!")
            all_ok = False
            continue
        
        with open(doc_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"\n{Colors.BOLD}{doc_file}:{Colors.END}")
        for section in required_sections:
            if section.lower() in content.lower():
                print_success(f"Section found: {section}")
            else:
                print_warning(f"Section might be missing: {section}")
    
    return all_ok, messages

def generate_report(results: Dict[str, Tuple[bool, List[str]]]):
    """Generate final report."""
    print_section("Validation Summary")
    
    total_checks = len(results)
    passed_checks = sum(1 for ok, _ in results.values() if ok)
    
    print(f"Total Checks: {total_checks}")
    print(f"Passed: {Colors.GREEN}{passed_checks}{Colors.END}")
    print(f"Failed: {Colors.RED}{total_checks - passed_checks}{Colors.END}")
    print()
    
    if passed_checks == total_checks:
        print_success("All validation checks passed!")
        print_info("Project is properly organized and functional ✨")
        return True
    else:
        print_error("Some validation checks failed")
        print_info("See messages above for details")
        
        # Collect all messages
        all_messages = []
        for messages in [m for _, m in results.values()]:
            all_messages.extend(messages)
        
        if all_messages:
            print("\n" + Colors.BOLD + "Action Items:" + Colors.END)
            for i, msg in enumerate(set(all_messages), 1):
                print(f"  {i}. {msg}")
        
        return False

def main():
    """Main validation function."""
    print(f"\n{Colors.BOLD}NeuroForge 3D - Project Validation{Colors.END}")
    print(f"{Colors.BOLD}Analyzing project structure and functionality...{Colors.END}\n")
    
    # Run all checks
    results = {
        "Directory Structure": check_directory_structure(),
        "Required Files": check_required_files(),
        "Python Syntax": check_python_syntax(),
        "Imports": check_imports(),
        "Documentation": check_documentation(),
    }
    
    # Generate final report
    success = generate_report(results)
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
