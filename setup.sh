#!/bin/bash
# NeuroForge 3D - Setup Script
# Organizes the project and ensures all dependencies are in place

set -e

echo "=========================================="
echo "NeuroForge 3D - Project Setup"
echo "=========================================="
echo ""

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored messages
print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_info() {
    echo -e "${YELLOW}ℹ${NC} $1"
}

# Check Python version
echo "1. Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
print_success "Python $PYTHON_VERSION found"
echo ""

# Create necessary directories
echo "2. Creating project directories..."
mkdir -p outputs
mkdir -p models
mkdir -p logs
mkdir -p tmp
print_success "Directories created: outputs/, models/, logs/, tmp/"
echo ""

# Check if virtual environment exists
echo "3. Checking virtual environment..."
if [ ! -d "venv" ]; then
    print_info "Virtual environment not found. Creating one..."
    python3 -m venv venv
    print_success "Virtual environment created"
else
    print_success "Virtual environment already exists"
fi
echo ""

# Activate virtual environment (for this script)
print_info "To activate the virtual environment, run:"
echo "    source venv/bin/activate  # Linux/Mac"
echo "    venv\\Scripts\\activate    # Windows"
echo ""

# Install dependencies (only if in virtual env)
if [ -n "$VIRTUAL_ENV" ]; then
    echo "4. Installing dependencies..."
    print_info "Upgrading pip..."
    pip install --upgrade pip setuptools wheel
    
    print_info "Installing basic dependencies..."
    # Install only basic dependencies that don't require CUDA
    pip install trimesh scipy numpy pillow
    
    print_success "Basic dependencies installed"
    echo ""
    
    print_info "For full installation with PyTorch and AI models:"
    echo "    pip install -r requirements.txt"
    echo "    # For CUDA support:"
    echo "    pip install torch==2.4.0 torchvision==0.19.0 --index-url https://download.pytorch.org/whl/cu121"
else
    print_info "Not in virtual environment. Skipping dependency installation."
    print_info "Activate venv first: source venv/bin/activate"
fi
echo ""

# Validate project structure
echo "5. Validating project structure..."
REQUIRED_FILES=(
    "src/__init__.py"
    "src/core/__init__.py"
    "src/core/base_generator.py"
    "src/core/mock_generator.py"
    "src/core/trellis_generator.py"
    "src/processing/__init__.py"
    "src/processing/pipeline.py"
    "src/ui/__init__.py"
    "src/ui/app.py"
    "launch_ui.py"
    "demo.py"
    "requirements.txt"
    "Dockerfile"
    "docker-compose.yml"
    "README.md"
    "QUICK_START.md"
)

ALL_FILES_EXIST=true
for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "$file" ]; then
        print_success "$file"
    else
        print_error "$file is missing!"
        ALL_FILES_EXIST=false
    fi
done
echo ""

if [ "$ALL_FILES_EXIST" = false ]; then
    print_error "Some required files are missing!"
    exit 1
fi

# Test basic imports
echo "6. Testing basic imports..."
if [ -n "$VIRTUAL_ENV" ]; then
    python3 -c "
import sys
sys.path.insert(0, 'src')
try:
    from core.base_generator import BaseGenerator
    from core.mock_generator import MockGenerator
    print('✓ Core modules import successfully')
except Exception as e:
    print(f'✗ Import error: {e}')
    sys.exit(1)
" || {
    print_error "Basic imports failed. Install dependencies: pip install trimesh scipy numpy"
    exit 1
}
    print_success "Basic imports working"
else
    print_info "Skipping import tests (not in virtual environment)"
fi
echo ""

# Summary
echo "=========================================="
echo "Setup Summary"
echo "=========================================="
print_success "Project directories created"
print_success "Project structure validated"
print_success "Basic setup complete"
echo ""

echo "Next Steps:"
echo "1. Activate virtual environment:"
echo "   source venv/bin/activate"
echo ""
echo "2. Install dependencies:"
echo "   pip install trimesh scipy numpy pytest  # For basic testing"
echo "   pip install -r requirements.txt        # For full features"
echo ""
echo "3. Run demo (basic test):"
echo "   python demo.py"
echo ""
echo "4. Or use Docker (recommended for GPU):"
echo "   docker-compose up --build"
echo ""
echo "5. For detailed setup instructions, see:"
echo "   QUICK_START.md"
echo ""

print_success "Setup complete! Project is organized and ready."
