# NeuroForge 3D - Text-to-STL Generator

> AI-powered system to generate printable 3D models from text prompts using Trellis/Hunyuan3D.

## 📖 Project Documentation

This project follows a structured development approach with detailed planning:

- **[PROJECT_CONTEXT.md](PROJECT_CONTEXT.md)** - Mission, stack, and architecture overview
- **[ROADMAP.md](ROADMAP.md)** - High-level development sprints (0-4)
- **[TECHNICAL_BLUEPRINT.md](TECHNICAL_BLUEPRINT.md)** - Detailed technical execution plan with 30 actionable work tickets
- **[CODING_STANDARDS.md](CODING_STANDARDS.md)** - AI agent coding guidelines

## 🚀 Quick Start

Follow the detailed instructions in [TECHNICAL_BLUEPRINT.md](TECHNICAL_BLUEPRINT.md) to begin development.

### Immediate First Steps (Sprint 0)

```bash
# 1. Create project structure
mkdir -p .github/workflows .devcontainer docs scripts src/{core,processing,ui,utils} tests models outputs

# 2. Set up Python environment
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install black ruff pytest

# 3. Start implementing Sprint 0 tasks
# See TECHNICAL_BLUEPRINT.md for detailed task breakdown
```

## 🏗️ Architecture

- **Core AI:** Microsoft TRELLIS or Hunyuan3D-2
- **Processing:** Trimesh (mesh repair and validation)
- **Infrastructure:** Docker with NVIDIA CUDA 12.1
- **Interface:** Gradio web UI + Blender Add-on

## 🛠️ Development Sprints

| Sprint | Focus | Tasks |
|--------|-------|-------|
| **Sprint 0** | Agentic Ecosystem Setup | 5 tasks |
| **Sprint 1** | Infrastructure & Mock Generator | 6 tasks |
| **Sprint 2** | AI Integration (Trellis/Hunyuan) | 6 tasks |
| **Sprint 3** | Mesh Processing Pipeline | 6 tasks |
| **Sprint 4** | UI & Blender Integration | 7 tasks |

**Total: 30 actionable work tickets** - See [TECHNICAL_BLUEPRINT.md](TECHNICAL_BLUEPRINT.md) for details.

## 🤖 Agentic Tools Integration

This project leverages AI-powered development tools:

- **Gemini Code Assist:** Automated code review on pull requests
- **Agentic Search AI:** Research latest documentation before coding
- **GitHub Actions:** Automated CI/CD pipeline

## 📋 Development Workflow

1. Review the task in [TECHNICAL_BLUEPRINT.md](TECHNICAL_BLUEPRINT.md)
2. Use Agentic Search (where indicated) to verify latest APIs/versions
3. Implement following [CODING_STANDARDS.md](CODING_STANDARDS.md)
4. Submit PR for Gemini Code Assist review
5. Validate with automated CI/CD

## 🎯 Success Metrics

- Docker images < 8GB
- Mesh processing with 90%+ repair success
- UI supports 10+ concurrent users
- Generated STLs are printable (watertight)

## 📚 Resources

- [Trimesh Documentation](https://trimsh.org/)
- [Gradio Documentation](https://gradio.app/docs/)
- [Blender Python API](https://docs.blender.org/api/current/)
- [HuggingFace Hub](https://huggingface.co/docs/hub/)

## 📝 License

[To be determined]

## 👥 Contributing

This is an early-stage project. Follow the technical blueprint for structured contribution.

---

**Status:** 🚧 In Development  
**Version:** 0.1.0-alpha  
**Last Updated:** November 2024
