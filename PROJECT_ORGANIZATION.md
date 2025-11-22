# Organização do Projeto NeuroForge 3D

## 📁 Estrutura de Diretórios

```
3dOpem2/
├── .github/              # GitHub Actions e configurações
├── blender_plugin/       # Plugin para Blender
│   ├── README.md         # Documentação do plugin
│   └── neuroforge_importer/
│       └── __init__.py   # Add-on do Blender
├── src/                  # Código fonte principal
│   ├── __init__.py       # Inicialização do pacote
│   ├── core/             # Geradores de modelos 3D
│   │   ├── __init__.py
│   │   ├── base_generator.py      # Classe base abstrata
│   │   ├── mock_generator.py      # Mock para testes
│   │   └── trellis_generator.py   # Gerador TRELLIS real
│   ├── processing/       # Processamento de malhas 3D
│   │   ├── __init__.py
│   │   ├── pipeline.py            # Pipeline completo
│   │   ├── mesh_repair.py         # Reparo de malhas
│   │   ├── mesh_scaling.py        # Escalonamento
│   │   └── mesh_validator.py      # Validação watertight
│   ├── ui/               # Interface web Gradio
│   │   ├── __init__.py
│   │   └── app.py                 # Aplicação Gradio
│   └── utils/            # Utilitários gerais
│       └── __init__.py
├── tests/                # Testes unitários
│   ├── __init__.py
│   ├── test_mock_generator.py
│   ├── test_processing.py
│   ├── test_trellis_generator.py
│   └── test_ui.py
├── outputs/              # Modelos gerados (gitignored)
├── models/               # Pesos dos modelos IA (gitignored)
├── logs/                 # Arquivos de log (gitignored)
├── tmp/                  # Arquivos temporários (gitignored)
├── demo.py               # Script de demonstração
├── launch_ui.py          # Launcher da interface web
├── examples_ui.py        # Exemplos de uso
├── setup.sh              # Script de configuração do projeto
├── validate_docker.sh    # Validação do Docker
├── requirements.txt      # Dependências Python
├── Dockerfile            # Imagem Docker
├── docker-compose.yml    # Orquestração Docker
├── .gitignore            # Arquivos ignorados pelo Git
├── .dockerignore         # Arquivos ignorados pelo Docker
├── README.md             # Documentação principal
├── QUICK_START.md        # Guia de início rápido
├── ARCHITECTURE.md       # Arquitetura do sistema
├── TECHNICAL_BLUEPRINT.md # Blueprint técnico
├── CODING_STANDARDS.md   # Padrões de código
├── ROADMAP.md            # Roadmap de desenvolvimento
├── PROJECT_CONTEXT.md    # Contexto do projeto
├── IMPLEMENTATION_SUMMARY.md # Resumo de implementação
└── SPRINT4_SUMMARY.md    # Resumo da Sprint 4

```

## 🎯 Componentes Principais

### 1. Geradores (`src/core/`)

- **BaseGenerator**: Classe base abstrata que define a interface
- **MockGenerator**: Implementação mock para testes sem IA
- **TrellisGenerator**: Gerador real usando Microsoft TRELLIS

### 2. Processamento (`src/processing/`)

- **Pipeline**: Orquestra todo o processamento de malhas
- **MeshRepair**: Repara malhas não-watertight
- **MeshScaling**: Normaliza escala para tamanho alvo
- **MeshValidator**: Valida se malha é imprimível

### 3. Interface Web (`src/ui/`)

- **NeuroForgeApp**: Aplicação Gradio para geração via web
- Suporta:
  - Entrada de prompts de texto
  - Configuração de tamanho alvo
  - Seed para reprodutibilidade
  - Visualização 3D interativa
  - Download de STL

### 4. Plugin Blender (`blender_plugin/`)

- **NeuroForge Importer**: Add-on para importar STLs no Blender
- Recursos:
  - Auto-refresh de arquivos
  - Centralização automática
  - Smooth shading
  - Configuração de diretório

## 🔧 Configuração do Ambiente

### Opção 1: Docker (Recomendado)

```bash
# Iniciar servidor com UI
docker-compose up --build

# Acessar em http://localhost:7860
```

### Opção 2: Instalação Local

```bash
# 1. Executar script de setup
./setup.sh

# 2. Ativar ambiente virtual
source venv/bin/activate

# 3. Instalar dependências básicas
pip install trimesh scipy numpy pytest

# 4. Testar instalação
python demo.py

# 5. (Opcional) Instalar dependências completas
pip install -r requirements.txt

# Para suporte CUDA:
pip install torch==2.4.0 torchvision==0.19.0 --index-url https://download.pytorch.org/whl/cu121
pip install xformers==0.0.27.post2 --index-url https://download.pytorch.org/whl/cu121
```

## 🧪 Validação e Testes

### Executar Testes

```bash
# Todos os testes
python -m pytest tests/ -v

# Testes específicos
python -m pytest tests/test_mock_generator.py -v

# Com cobertura
python -m pytest tests/ --cov=src --cov-report=html
```

### Demo Script

```bash
# Demonstra funcionalidade básica
python demo.py

# Gera:
# - outputs/demo_cube.stl
# - outputs/demo_box.stl
# - outputs/demo_sphere.stl
# - outputs/demo_cylinder.stl
# - outputs/demo_scaled.stl
```

### Validação Docker

```bash
# Valida configuração Docker
./validate_docker.sh
```

## 📊 Fluxo de Trabalho

### Geração de Modelo 3D

```
Prompt → TrellisGenerator → Malha Raw → Pipeline → STL Watertight
           ↓
    1. Text-to-Image (SDXL)
    2. Remove Background (rembg)
    3. Image-to-3D (TRELLIS)
                                         ↓
                                  1. Validação
                                  2. Reparo
                                  3. Escala
                                  4. Exportação
```

### Interface Web (Gradio)

```
Usuário → Web UI → NeuroForgeApp → TrellisGenerator → Pipeline → STL Download
          ↓
    - Prompt input
    - Size config
    - Seed (opcional)
                      ↓
                - Queue management
                - Progress tracking
                - 3D viewer
```

### Integração Blender

```
STL em outputs/ → Plugin Refresh → Seleção → Import → Blender Scene
                                                 ↓
                                        - Auto-center
                                        - Smooth shading
                                        - Ready to edit
```

## 🔍 Checklist de Funcionalidade

### ✅ Funcionalidades Implementadas

- [x] Estrutura de projeto organizada
- [x] Geradores (base, mock, trellis)
- [x] Pipeline de processamento 3D
- [x] Validação watertight
- [x] Reparo de malhas
- [x] Normalização de escala
- [x] Interface web Gradio
- [x] Plugin Blender
- [x] Docker + docker-compose
- [x] Testes unitários
- [x] Documentação completa
- [x] Scripts de setup e validação

### 🔄 Melhorias Futuras (v2.0)

- [ ] Quantização de modelos (GGUF/ONNX)
- [ ] Galeria de prompts
- [ ] API REST
- [ ] CLI tool
- [ ] Batch processing
- [ ] Material presets (Blender)
- [ ] Auto-UV unwrapping

## 📚 Documentação

### Documentos Principais

1. **README.md** - Documentação geral do projeto
2. **QUICK_START.md** - Guia de início rápido (primeiro voo)
3. **ARCHITECTURE.md** - Arquitetura do sistema
4. **TECHNICAL_BLUEPRINT.md** - Blueprint técnico detalhado
5. **blender_plugin/README.md** - Guia do plugin Blender

### Documentos Técnicos

- **CODING_STANDARDS.md** - Padrões de código
- **PROJECT_CONTEXT.md** - Contexto e stack tecnológica
- **ROADMAP.md** - Roadmap de sprints
- **SPRINT4_SUMMARY.md** - Resumo da Sprint 4
- **IMPLEMENTATION_SUMMARY.md** - Resumos de implementação

## 🛠️ Solução de Problemas

### Problemas Comuns

1. **Módulos não encontrados**
   ```bash
   # Solução: Instalar dependências
   pip install trimesh scipy numpy
   # ou
   pip install -r requirements.txt
   ```

2. **Diretórios outputs/models não existem**
   ```bash
   # Solução: Executar setup
   ./setup.sh
   # ou manualmente
   mkdir -p outputs models logs tmp
   ```

3. **Docker não inicia GPU**
   ```bash
   # Verificar suporte GPU
   docker run --rm --gpus all nvidia/cuda:12.1.0-base-ubuntu22.04 nvidia-smi
   ```

4. **Blender não encontra arquivos**
   - Verificar configuração do diretório no plugin
   - Clicar em "Refresh" para atualizar lista
   - Verificar mapeamento de volumes no Docker

## 🎓 Recursos de Aprendizado

### Para Desenvolvedores

1. Ler `TECHNICAL_BLUEPRINT.md` para entender a arquitetura
2. Estudar `src/core/base_generator.py` para interface de geradores
3. Examinar `src/processing/pipeline.py` para processamento
4. Ver `tests/` para exemplos de uso

### Para Usuários

1. Seguir `QUICK_START.md` para setup inicial
2. Ler `README.md` seção de uso
3. Ver `blender_plugin/README.md` para Blender
4. Executar `demo.py` para exemplos práticos

## 📝 Contribuindo

### Antes de Contribuir

1. Ler `CODING_STANDARDS.md`
2. Executar testes: `pytest tests/ -v`
3. Validar código: `python -m py_compile src/**/*.py`
4. Atualizar documentação se necessário

### Fluxo de Contribuição

1. Fork do repositório
2. Criar branch: `git checkout -b feature/nome-da-feature`
3. Fazer mudanças e testar
4. Commit: `git commit -m 'Add feature'`
5. Push: `git push origin feature/nome-da-feature`
6. Abrir Pull Request

## 🔐 Segurança

- Modelos de IA são baixados em `models/` (não versionado)
- Outputs em `outputs/` (não versionado)
- Logs em `logs/` (não versionado)
- Variáveis de ambiente em `.env` (não versionado)
- CodeQL scan em PRs para vulnerabilidades

## 📦 Dependências

### Dependências Core

- **PyTorch 2.4.0** - Framework de deep learning
- **Trimesh 4.4.9** - Processamento de malhas 3D
- **Gradio 5.11.0** - Interface web
- **Transformers 4.48.0** - Modelos de linguagem
- **Diffusers 0.30.3** - Modelos de difusão

### Dependências de Desenvolvimento

- **pytest** - Testes unitários
- **black** - Formatação de código
- **flake8** - Linting
- **mypy** - Type checking

Ver `requirements.txt` para lista completa.

---

**Versão:** 1.0.0  
**Última Atualização:** 2025-11-22  
**Status:** Funcional e Organizado ✅
