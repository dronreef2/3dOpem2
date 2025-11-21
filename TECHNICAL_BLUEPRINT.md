# TECHNICAL BLUEPRINT: NeuroForge 3D
## Detailed Execution Plan (Sprint 0 → 4)

> **Role:** Technical Product Manager & Senior DevOps Engineer  
> **Context:** Text-to-STL project using Trellis/Hunyuan3D with integrated Agentic Tools  
> **Tools Available:** Agentic Search, Gemini Code Assist, GitHub Actions  
> **References:** [PROJECT_CONTEXT.md](PROJECT_CONTEXT.md), [ROADMAP.md](ROADMAP.md)

---

## 🛠️ SPRINT 0: Configuração do Ecossistema Agentic

**Objetivo:** Ativar ferramentas de IA no GitHub e preparar ambiente de desenvolvimento.

### Tabela de Tarefas

| ID | Título Técnico | Descrição da Implementação | Critério de Aceite (DoD) | Verificação Agentic |
|---|---|---|---|---|
| **S0-T01** | Configurar GitHub Action para Gemini Code Review | Criar arquivo `.github/workflows/gemini-review.yml` que escuta eventos `pull_request` e aciona o Gemini Code Assist para análise automática de código.<br><br>**Implementação:**<br>- Criar diretório `.github/workflows/`<br>- Adicionar workflow com triggers: `[opened, synchronize, reopened]`<br>- Configurar permissões: `contents: read`, `pull-requests: write`<br>- Usar action oficial do Gemini ou script custom com API | • O arquivo `.github/workflows/gemini-review.yml` existe<br>• Ao abrir um PR de teste, o workflow é executado (verificar na aba Actions do GitHub)<br>• O bot do Gemini comenta no PR (ou não retorna erro de autenticação) | **Usar Agentic Search para:**<br>- "GitHub Action for Gemini Code Assist yaml syntax latest 2024"<br>- "How to integrate Google Gemini API with GitHub Actions pull request" |
| **S0-T02** | Configurar DevContainer para VS Code | Criar arquivo `.devcontainer/devcontainer.json` para ambiente de desenvolvimento consistente.<br><br>**Implementação:**<br>- Base image: `mcr.microsoft.com/devcontainers/python:3.11`<br>- Features: Git, GitHub CLI, CUDA Toolkit (opcional para local)<br>- Extensions: Python, Pylance, GitLens<br>- PostCreateCommand: `pip install -r requirements.txt` (quando existir) | • O arquivo `.devcontainer/devcontainer.json` existe<br>• VS Code consegue abrir o projeto no container (opção "Reopen in Container")<br>• Terminal dentro do container tem acesso ao Python 3.11+ | **Usar Agentic Search para:**<br>- "VS Code devcontainer.json best practices Python ML project 2024" |
| **S0-T03** | Configurar ambiente Python local (alternativa) | Criar script `setup_env.sh` para inicialização rápida do ambiente virtual.<br><br>**Implementação:**<br>- Script deve criar venv: `python3 -m venv .venv`<br>- Ativar venv e instalar ferramentas base: `pip install black ruff pytest`<br>- Adicionar `.venv/` ao `.gitignore` | • Ao executar `bash setup_env.sh`, um ambiente virtual é criado<br>• O comando `source .venv/bin/activate` funciona<br>• `which python` aponta para `.venv/bin/python` | Não requer Agentic Search (tarefa simples) |
| **S0-T04** | Criar Workflow de CI para Build Validation | Criar `.github/workflows/ci.yml` que valida sintaxe Python e roda testes básicos.<br><br>**Implementação:**<br>- Trigger: `push` e `pull_request`<br>- Jobs: `lint` (ruff/black), `test` (pytest quando houver testes)<br>- Matrix strategy: Python 3.10, 3.11 | • O workflow `.github/workflows/ci.yml` existe<br>• Ao fazer push, o workflow é executado sem erros<br>• Badge do CI pode ser adicionado ao README (opcional) | **Usar Agentic Search para:**<br>- "GitHub Actions matrix strategy Python black ruff pytest template" |
| **S0-T05** | Testar Agentic Search (Validação de Integração) | Criar um documento de teste `docs/AGENTIC_SEARCH_TEST.md` onde você solicita ao Agentic Search para resumir a documentação do repositório `microsoft/TRELLIS`.<br><br>**Implementação:**<br>- Criar pasta `docs/`<br>- Documentar o resultado da pesquisa Agentic sobre Trellis<br>- Incluir: versão atual, requisitos de sistema, link para HuggingFace | • O arquivo `docs/AGENTIC_SEARCH_TEST.md` contém informações atualizadas sobre o TRELLIS<br>• As informações incluem links válidos para pesos do modelo | **USAR AGORA:**<br>- "Microsoft TRELLIS GitHub repository latest release 2024"<br>- "TRELLIS model weights HuggingFace download link" |

---

## 🏁 SPRINT 1: A Fundação (Infraestrutura & Mock)

**Objetivo:** Criar estrutura Docker otimizada e pipeline "dummy" com classe abstrata.

### Tabela de Tarefas

| ID | Título Técnico | Descrição da Implementação | Critério de Aceite (DoD) | Verificação Agentic |
|---|---|---|---|---|
| **S1-T01** | Criar Dockerfile Multi-Stage | Criar `Dockerfile` otimizado para reduzir tamanho da imagem final.<br><br>**Implementação:**<br>- **Stage 1 (builder):** `FROM nvidia/cuda:12.1.0-devel-ubuntu22.04`<br>  - Instalar dependências de build: `build-essential`, `python3-dev`<br>  - Copiar `requirements.txt` e instalar via pip<br>- **Stage 2 (runtime):** `FROM nvidia/cuda:12.1.0-runtime-ubuntu22.04`<br>  - Copiar apenas arquivos necessários do builder<br>  - Copiar código da aplicação de `src/`<br>- WORKDIR: `/app`<br>- CMD: `["python", "src/main.py"]` (quando existir) | • O arquivo `Dockerfile` existe<br>• `docker build -t neuroforge3d .` executa sem erros<br>• O tamanho da imagem final é < 8GB (verificar com `docker images`)<br>• `docker run --rm neuroforge3d --help` não retorna erro (quando main.py existir) | **Usar Agentic Search para:**<br>- "NVIDIA CUDA Docker multi-stage build best practices 2024"<br>- "Reduce Docker image size Python ML application" |
| **S1-T02** | Criar requirements.txt com versões travadas | Criar `requirements.txt` com dependências principais e versões fixas.<br><br>**Implementação:**<br>Incluir (com versões a pesquisar):<br>- `torch==2.x.x` (compatível com CUDA 12.1)<br>- `trimesh==4.x.x`<br>- `numpy==1.26.x`<br>- `gradio==4.x.x`<br>- `pillow==10.x.x`<br>- `huggingface-hub==0.20.x`<br><br>Usar formato: `package==X.Y.Z` (sem `>=`) | • O arquivo `requirements.txt` existe<br>• Todas as dependências têm versões fixas (nenhum `>=` ou `~=`)<br>• `pip install -r requirements.txt` executa sem conflitos de versão | **Usar Agentic Search para:**<br>- "PyTorch latest version compatible with CUDA 12.1"<br>- "Trimesh latest stable version 2024"<br>- "Gradio latest stable version November 2024" |
| **S1-T03** | Implementar Classe Abstrata BaseGenerator | Criar `src/core/base_generator.py` com interface abstrata para geradores 3D.<br><br>**Implementação:**<br>```python<br>from abc import ABC, abstractmethod<br>from pathlib import Path<br>import trimesh<br><br>class BaseGenerator(ABC):<br>    """Interface abstrata para geradores Text-to-3D."""<br>    <br>    @abstractmethod<br>    def generate(self, prompt: str, output_path: Path) -> trimesh.Trimesh:<br>        """Gera modelo 3D a partir do prompt."""<br>        pass<br>    <br>    @abstractmethod<br>    def validate_mesh(self, mesh: trimesh.Trimesh) -> bool:<br>        """Valida se a mesh é printable (watertight)."""<br>        pass<br>```<br>Usar Type Hints e docstrings detalhadas. | • O arquivo `src/core/base_generator.py` existe<br>• A classe `BaseGenerator` é abstrata (herda de ABC)<br>• Métodos `generate` e `validate_mesh` estão decorados com `@abstractmethod`<br>• Código passa no `ruff check src/` | Não requer Agentic Search (padrão conhecido) |
| **S1-T04** | Implementar MockGenerator (Cubo Simples) | Criar `src/core/mock_generator.py` que herda de `BaseGenerator` e retorna um cubo via trimesh.<br><br>**Implementação:**<br>```python<br>import trimesh<br>from pathlib import Path<br>from .base_generator import BaseGenerator<br><br>class MockGenerator(BaseGenerator):<br>    def generate(self, prompt: str, output_path: Path) -> trimesh.Trimesh:<br>        """Retorna um cubo de 50mm."""<br>        mesh = trimesh.creation.box(extents=[50, 50, 50])<br>        mesh.export(output_path)<br>        return mesh<br>    <br>    def validate_mesh(self, mesh: trimesh.Trimesh) -> bool:<br>        return mesh.is_watertight<br>```<br>Adicionar logging usando `import logging`. | • O arquivo `src/core/mock_generator.py` existe<br>• Instanciar `MockGenerator().generate("test", Path("test.stl"))` cria um arquivo STL válido<br>• `validate_mesh` retorna `True` para o cubo gerado<br>• Código passa em `ruff` e `black` | Não requer Agentic Search |
| **S1-T05** | Criar estrutura de diretórios do projeto | Criar a estrutura completa de pastas para organização do código.<br><br>**Implementação:**<br>```<br>src/<br>  core/<br>    __init__.py<br>    base_generator.py<br>    mock_generator.py<br>  processing/<br>    __init__.py<br>  ui/<br>    __init__.py<br>  utils/<br>    __init__.py<br>tests/<br>  __init__.py<br>  test_mock_generator.py<br>models/<br>  .gitkeep<br>outputs/<br>  .gitkeep<br>```<br>Adicionar `models/` e `outputs/` ao `.gitignore` (exceto .gitkeep). | • Todos os diretórios listados existem<br>• Arquivos `__init__.py` estão presentes nos módulos Python<br>• `.gitignore` contém `models/*` e `outputs/*` (mas não `.gitkeep`) | Não requer Agentic Search |
| **S1-T06** | Criar GitHub Action para Build Automático | Criar `.github/workflows/docker-build.yml` para build automático do container.<br><br>**Implementação:**<br>- Trigger: `push` em branches `main` e `develop`<br>- Job: Build da imagem Docker<br>- Usar cache do Docker Layer Caching<br>- (Opcional) Push para GitHub Container Registry | • O workflow existe<br>• Ao fazer push em `main`, o build do Docker é executado<br>• O build completa sem erros (verificar no Actions) | **Usar Agentic Search para:**<br>- "GitHub Actions Docker build cache optimization 2024" |

---

## 🧠 SPRINT 2: O Cérebro (Integração de IA)

**Objetivo:** Integrar modelo Trellis/Hunyuan3D com gestão eficiente de VRAM.

### Tabela de Tarefas

| ID | Título Técnico | Descrição da Implementação | Critério de Aceite (DoD) | Verificação Agentic |
|---|---|---|---|---|
| **S2-T01** | Implementar TrellisGenerator (Estrutura Inicial) | Criar `src/core/trellis_generator.py` que herda de `BaseGenerator`.<br><br>**Implementação:**<br>```python<br>from .base_generator import BaseGenerator<br>import torch<br>from pathlib import Path<br><br>class TrellisGenerator(BaseGenerator):<br>    def __init__(self, model_path: Path, device: str = "cuda"):<br>        self.device = device<br>        self.model_path = model_path<br>        self.model = None  # Lazy loading<br>    <br>    def _load_model(self):<br>        """Carrega modelo com cpu_offload se VRAM < 12GB."""<br>        # Implementar lógica de detecção de VRAM<br>        # Usar torch.cuda.get_device_properties()<br>        pass<br>    <br>    def generate(self, prompt: str, output_path: Path) -> trimesh.Trimesh:<br>        # TODO: Implementar pipeline Trellis<br>        raise NotImplementedError<br>```<br>Adicionar gestão de memória. | • O arquivo `src/core/trellis_generator.py` existe<br>• A classe herda corretamente de `BaseGenerator`<br>• Método `_load_model` detecta VRAM disponível<br>• Código passa no linting | **Usar Agentic Search para:**<br>- "PyTorch detect GPU VRAM available programmatically"<br>- "CUDA memory management best practices Python" |
| **S2-T02** | Pesquisar URL dos Pesos do Modelo Trellis | Usar Agentic Search para encontrar a localização correta dos pesos no HuggingFace.<br><br>**Implementação:**<br>- Documentar em `docs/MODEL_WEIGHTS.md` as URLs encontradas<br>- Incluir: nome do modelo, tamanho, hash de verificação (se disponível)<br>- Adicionar exemplo de comando `huggingface-cli download` | • `docs/MODEL_WEIGHTS.md` existe e contém:<br>  - URL do HuggingFace para Trellis<br>  - Comando de download funcional<br>  - Tamanho estimado do modelo | **USAR AGORA:**<br>- "Microsoft TRELLIS HuggingFace model weights download URL 2024"<br>- "TRELLIS model checkpoint location" |
| **S2-T03** | Criar Script de Download de Pesos | Criar `scripts/download_models.py` para baixar pesos automaticamente.<br><br>**Implementação:**<br>```python<br>from huggingface_hub import hf_hub_download<br>from pathlib import Path<br>import logging<br><br>def download_trellis(cache_dir: Path = Path("models/")):<br>    """Baixa pesos do Trellis do HuggingFace."""<br>    # Usar informações de S2-T02<br>    model_id = "microsoft/trellis-xxx"  # Pesquisar<br>    filename = "model.safetensors"  # Pesquisar<br>    <br>    hf_hub_download(<br>        repo_id=model_id,<br>        filename=filename,<br>        cache_dir=cache_dir<br>    )<br>```<br>Adicionar barra de progresso com `tqdm`. | • `scripts/download_models.py` existe<br>• Executar `python scripts/download_models.py` baixa os pesos para `models/`<br>• O script exibe progresso do download<br>• Pesos baixados são verificados (checksum se disponível) | **Usar Agentic Search para:**<br>- "huggingface_hub download with progress bar Python" |
| **S2-T04** | Implementar Lógica de CPU Offload | Adicionar no `TrellisGenerator` lógica para economizar VRAM.<br><br>**Implementação:**<br>```python<br>def _load_model(self):<br>    vram_gb = torch.cuda.get_device_properties(0).total_memory / 1e9<br>    <br>    if vram_gb < 12:<br>        # Usar accelerate para cpu_offload<br>        from accelerate import cpu_offload<br>        self.model = load_model(self.model_path)<br>        cpu_offload(self.model, execution_device=0)<br>    else:<br>        self.model = load_model(self.model_path).to(self.device)<br>```<br>Documentar threshold de VRAM no docstring. | • A lógica de `_load_model` detecta VRAM corretamente<br>• Em GPU com <12GB, `cpu_offload` é usado<br>• Em GPU com ≥12GB, modelo fica totalmente na GPU<br>• Teste manual: forçar `vram_gb = 8` e verificar que cpu_offload é chamado | **Usar Agentic Search para:**<br>- "HuggingFace Accelerate cpu_offload tutorial 2024"<br>- "Optimize VRAM usage large diffusion models" |
| **S2-T05** | Implementar Pipeline de Geração (Integração Real) | Completar método `generate()` do `TrellisGenerator` com pipeline real.<br><br>**Implementação:**<br>- Carregar modelo via `_load_model()`<br>- Processar prompt: tokenização e embedding<br>- Executar inferência: `model(prompt_embedding)`<br>- Converter saída para nuvem de pontos<br>- Converter para mesh via Marching Cubes (se necessário)<br>- Salvar como STL usando `trimesh.export()`<br><br>Adicionar tratamento de erros. | • Executar `TrellisGenerator().generate("a cat", Path("cat.stl"))` cria um arquivo STL<br>• O arquivo STL é válido (abre no MeshLab ou Blender)<br>• Logs informativos são gerados durante o processo<br>• Tempo de inferência é registrado | **Usar Agentic Search para:**<br>- "TRELLIS model inference pipeline Python example"<br>- "Convert point cloud to mesh Python trimesh" |
| **S2-T06** | Adicionar Testes de Integração para Trellis | Criar `tests/test_trellis_generator.py` com testes básicos.<br><br>**Implementação:**<br>```python<br>import pytest<br>from src.core.trellis_generator import TrellisGenerator<br>from pathlib import Path<br><br>@pytest.mark.skipif(not torch.cuda.is_available(), reason="Requires GPU")<br>def test_trellis_generate():<br>    gen = TrellisGenerator(Path("models/trellis"))<br>    mesh = gen.generate("simple cube", Path("test_output.stl"))<br>    assert mesh.is_watertight<br>```<br>Usar fixtures para evitar downloads repetidos. | • `tests/test_trellis_generator.py` existe<br>• `pytest tests/test_trellis_generator.py` executa sem erros (em ambiente com GPU)<br>• Teste é skipado automaticamente se CUDA não disponível | Não requer Agentic Search |

---

## ⚙️ SPRINT 3: A Engenharia (Mesh Processing)

**Objetivo:** Transformar geometria bruta em sólidos prontos para impressão 3D.

### Tabela de Tarefas

| ID | Título Técnico | Descrição da Implementação | Critério de Aceite (DoD) | Verificação Agentic |
|---|---|---|---|---|
| **S3-T01** | Implementar Pipeline de Reparo de Malha | Criar `src/processing/mesh_repair.py` com funções de reparo.<br><br>**Implementação:**<br>```python<br>import trimesh<br>import logging<br><br>def repair_mesh(mesh: trimesh.Trimesh) -> trimesh.Trimesh:<br>    """<br>    Repara malha para torná-la watertight.<br>    <br>    Steps:<br>    1. Verifica se já é watertight<br>    2. Se não: trimesh.repair.fill_holes()<br>    3. Se ainda não: trimesh.repair.fix_normals()<br>    4. Remove componentes desconexos pequenos<br>    """<br>    if mesh.is_watertight:<br>        return mesh<br>    <br>    logging.info("Mesh não é watertight. Iniciando reparo...")<br>    mesh.fill_holes()<br>    mesh.fix_normals()<br>    <br>    # Remover componentes com < 5% dos vértices<br>    mesh = mesh.split(only_watertight=False)[0]<br>    <br>    return mesh<br>```<br>Adicionar validação final. | • `src/processing/mesh_repair.py` existe<br>• Função `repair_mesh()` retorna uma mesh watertight para casos de teste<br>• Teste: Mesh quebrada → `repair_mesh()` → `is_watertight == True`<br>• Código passa no linting | **Usar Agentic Search para:**<br>- "Trimesh repair mesh watertight best practices"<br>- "Fix non-manifold mesh Python" |
| **S3-T02** | Implementar Lógica de Normalização de Escala | Criar `src/processing/mesh_scaling.py` para normalizar malhas.<br><br>**Implementação:**<br>```python<br>import trimesh<br>import numpy as np<br><br>def normalize_scale(mesh: trimesh.Trimesh, target_size_mm: float = 100.0) -> trimesh.Trimesh:<br>    """<br>    Normaliza mesh para bounding box de target_size_mm.<br>    <br>    Args:<br>        mesh: Mesh de entrada<br>        target_size_mm: Tamanho alvo da maior dimensão (padrão: 100mm)<br>    <br>    Returns:<br>        Mesh escalada<br>    """<br>    bounds = mesh.bounds  # [[min_x, min_y, min_z], [max_x, max_y, max_z]]<br>    current_size = (bounds[1] - bounds[0]).max()<br>    scale_factor = target_size_mm / current_size<br>    <br>    mesh.apply_scale(scale_factor)<br>    return mesh<br>```<br>Adicionar opção de centralizar mesh na origem. | • `src/processing/mesh_scaling.py` existe<br>• Mesh de 200mm normalizada → bounding box max = 100mm (±0.1mm)<br>• Mesh mantém proporções (aspect ratio preservado)<br>• Centro da mesh está em (0,0,0) se opção ativada | Não requer Agentic Search |
| **S3-T03** | Implementar Validador de Manifold | Criar `src/processing/mesh_validator.py` com verificações rigorosas.<br><br>**Implementação:**<br>```python<br>import trimesh<br>from typing import Dict, List<br><br>def validate_for_printing(mesh: trimesh.Trimesh) -> Dict[str, any]:<br>    """<br>    Valida mesh para impressão 3D.<br>    <br>    Returns:<br>        Dict com:<br>        - is_valid: bool<br>        - errors: List[str]<br>        - warnings: List[str]<br>        - stats: Dict (volume, área, etc.)<br>    """<br>    errors = []<br>    warnings = []<br>    <br>    if not mesh.is_watertight:<br>        errors.append("Mesh não é watertight")<br>    <br>    if mesh.body_count > 1:<br>        warnings.append(f"Mesh tem {mesh.body_count} componentes desconexos")<br>    <br>    if mesh.volume <= 0:<br>        errors.append("Volume da mesh é inválido")<br>    <br>    stats = {<br>        "volume_mm3": mesh.volume,<br>        "area_mm2": mesh.area,<br>        "vertices": len(mesh.vertices),<br>        "faces": len(mesh.faces)<br>    }<br>    <br>    return {<br>        "is_valid": len(errors) == 0,<br>        "errors": errors,<br>        "warnings": warnings,<br>        "stats": stats<br>    }<br>```<br>Adicionar verificação de auto-interseções. | • `src/processing/mesh_validator.py` existe<br>• Cubo simples passa na validação (`is_valid == True`)<br>• Mesh quebrada retorna erros específicos<br>• Stats são calculados corretamente | **Usar Agentic Search para:**<br>- "Trimesh detect self intersections"<br>- "3D printing mesh validation checklist" |
| **S3-T04** | Criar Pipeline Completo de Processamento | Criar `src/processing/pipeline.py` que integra reparo + escala + validação.<br><br>**Implementação:**<br>```python<br>from .mesh_repair import repair_mesh<br>from .mesh_scaling import normalize_scale<br>from .mesh_validator import validate_for_printing<br>import trimesh<br>from pathlib import Path<br>import logging<br><br>class ProcessingPipeline:<br>    """Pipeline completo de pós-processamento."""<br>    <br>    def __init__(self, target_size_mm: float = 100.0):<br>        self.target_size = target_size_mm<br>    <br>    def process(self, mesh: trimesh.Trimesh, output_path: Path) -> Dict:<br>        """Executa pipeline completo."""<br>        logging.info("Iniciando pipeline de processamento...")<br>        <br>        # 1. Reparar<br>        mesh = repair_mesh(mesh)<br>        <br>        # 2. Normalizar escala<br>        mesh = normalize_scale(mesh, self.target_size)<br>        <br>        # 3. Validar<br>        validation = validate_for_printing(mesh)<br>        <br>        if validation["is_valid"]:<br>            mesh.export(output_path)<br>            logging.info(f"Mesh processada salva em {output_path}")<br>        else:<br>            logging.error(f"Mesh inválida: {validation['errors']}")<br>        <br>        return validation<br>```<br>Adicionar opções configuráveis. | • `src/processing/pipeline.py` existe<br>• Pipeline processa mesh do início ao fim sem erros<br>• Arquivo STL final é válido e watertight<br>• Validação retorna stats corretos | Não requer Agentic Search |
| **S3-T05** | Integrar Pipeline no BaseGenerator | Modificar `BaseGenerator` para usar o pipeline automaticamente.<br><br>**Implementação:**<br>Atualizar `src/core/base_generator.py`:<br>```python<br>from src.processing.pipeline import ProcessingPipeline<br><br>class BaseGenerator(ABC):<br>    def __init__(self):<br>        self.pipeline = ProcessingPipeline(target_size_mm=100.0)<br>    <br>    @abstractmethod<br>    def _generate_raw(self, prompt: str) -> trimesh.Trimesh:<br>        """Gera mesh bruta (pode não ser watertight)."""<br>        pass<br>    <br>    def generate(self, prompt: str, output_path: Path) -> Dict:<br>        """Gera + processa mesh."""<br>        raw_mesh = self._generate_raw(prompt)<br>        return self.pipeline.process(raw_mesh, output_path)<br>```<br>Atualizar MockGenerator e TrellisGenerator. | • Método `generate()` agora retorna validação do pipeline<br>• `MockGenerator` e `TrellisGenerator` implementam `_generate_raw()`<br>• Teste end-to-end: geração → processamento → validação funciona<br>• Código passa no linting | Não requer Agentic Search |
| **S3-T06** | Criar Testes para Pipeline de Processamento | Criar `tests/test_processing_pipeline.py` com casos de teste.<br><br>**Implementação:**<br>```python<br>import pytest<br>import trimesh<br>from src.processing.pipeline import ProcessingPipeline<br>from pathlib import Path<br><br>def test_pipeline_valid_mesh():<br>    """Testa pipeline com mesh válida."""<br>    mesh = trimesh.creation.box(extents=[10, 10, 10])<br>    pipeline = ProcessingPipeline(target_size_mm=50.0)<br>    result = pipeline.process(mesh, Path("/tmp/test.stl"))<br>    assert result["is_valid"] is True<br><br>def test_pipeline_repairs_broken_mesh():<br>    """Testa que pipeline repara mesh quebrada."""<br>    # Criar mesh com buracos<br>    mesh = create_broken_mesh()  # Helper function<br>    pipeline = ProcessingPipeline()<br>    result = pipeline.process(mesh, Path("/tmp/repaired.stl"))<br>    # Verificar que foi reparada<br>```<br>Adicionar fixtures. | • `tests/test_processing_pipeline.py` existe<br>• `pytest tests/test_processing_pipeline.py` passa todos os testes<br>• Cobertura de código > 80% para módulo processing | Não requer Agentic Search |

---

## 🖥️ SPRINT 4: Entrega (UI & Integração)

**Objetivo:** Interface Gradio com fila e Add-on para Blender.

### Tabela de Tarefas

| ID | Título Técnico | Descrição da Implementação | Critério de Aceite (DoD) | Verificação Agentic |
|---|---|---|---|---|
| **S4-T01** | Implementar Interface Gradio Básica | Criar `src/ui/gradio_app.py` com interface web.<br><br>**Implementação:**<br>```python<br>import gradio as gr<br>from src.core.trellis_generator import TrellisGenerator<br>from pathlib import Path<br><br>def generate_3d(prompt: str, model_choice: str) -> str:<br>    """Gera modelo 3D e retorna caminho do arquivo."""<br>    if model_choice == "Mock":<br>        from src.core.mock_generator import MockGenerator<br>        gen = MockGenerator()<br>    else:<br>        gen = TrellisGenerator(Path("models/trellis"))<br>    <br>    output_path = Path(f"outputs/{prompt[:20]}.stl")<br>    gen.generate(prompt, output_path)<br>    return str(output_path)<br><br>demo = gr.Interface(<br>    fn=generate_3d,<br>    inputs=[<br>        gr.Textbox(label="Prompt", placeholder="a futuristic chair"),<br>        gr.Radio(["Mock", "Trellis"], label="Model", value="Mock")<br>    ],<br>    outputs=gr.File(label="Download STL"),<br>    title="NeuroForge 3D: Text-to-STL",<br>    description="Generate printable 3D models from text"<br>)<br>```<br>Adicionar preview 3D se possível. | • `src/ui/gradio_app.py` existe<br>• Executar `python src/ui/gradio_app.py` abre interface no navegador<br>• Submeter prompt gera arquivo STL para download<br>• Interface é responsiva e intuitiva | **Usar Agentic Search para:**<br>- "Gradio 3D model viewer component 2024"<br>- "Gradio file download output" |
| **S4-T02** | Adicionar Sistema de Fila (Queue) | Modificar `gradio_app.py` para suportar múltiplos usuários.<br><br>**Implementação:**<br>```python<br>demo = gr.Interface(<br>    # ... configuração anterior<br>).queue(<br>    max_size=10,  # Máximo de 10 requisições na fila<br>    default_concurrency_limit=2  # Processa 2 por vez<br>)<br><br>if __name__ == "__main__":<br>    demo.launch(<br>        server_name="0.0.0.0",<br>        server_port=7860,<br>        share=False<br>    )<br>```<br>Adicionar indicador de posição na fila. | • Interface não trava ao receber múltiplas requisições simultâneas<br>• Fila é visível para o usuário (posição na fila)<br>• Limite de concorrência é respeitado<br>• Teste: enviar 5 requisições simultaneamente → todas são processadas | **Usar Agentic Search para:**<br>- "Gradio queue configuration best practices"<br>- "Gradio handle multiple concurrent requests" |
| **S4-T03** | Adicionar Visualização 3D na Interface | Integrar componente de preview 3D no Gradio.<br><br>**Implementação:**<br>```python<br>outputs=[<br>    gr.Model3D(label="Preview 3D"),  # Novo em Gradio 4.x<br>    gr.File(label="Download STL")<br>]<br><br>def generate_3d(prompt: str, model_choice: str) -> Tuple[str, str]:<br>    # ... gerar mesh<br>    return str(output_path), str(output_path)  # Para preview e download<br>```<br>Verificar compatibilidade do formato STL. | • Preview 3D é exibido na interface após geração<br>• Usuário pode rotacionar/zoom no modelo 3D<br>• Botão de download funciona independentemente do preview | **Usar Agentic Search para:**<br>- "Gradio Model3D component STL support"<br>- "Display 3D mesh in Gradio interface" |
| **S4-T04** | Criar Blender Add-on (Estrutura) | Criar `blender_addon/neuroforge3d/__init__.py` com add-on básico.<br><br>**Implementação:**<br>```python<br>bl_info = {<br>    "name": "NeuroForge 3D Importer",<br>    "author": "NeuroForge Team",<br>    "version": (1, 0, 0),<br>    "blender": (3, 6, 0),<br>    "location": "File > Import > NeuroForge 3D",<br>    "description": "Import AI-generated STL models",<br>    "category": "Import-Export",<br>}<br><br>import bpy<br>from bpy.types import Operator<br>from bpy_extras.io_utils import ImportHelper<br><br>class ImportNeuroForge3D(Operator, ImportHelper):<br>    bl_idname = "import_scene.neuroforge3d"<br>    bl_label = "Import NeuroForge STL"<br>    filename_ext = ".stl"<br>    <br>    def execute(self, context):<br>        # Usar bpy.ops.import_mesh.stl()<br>        bpy.ops.import_mesh.stl(filepath=self.filepath)<br>        return {'FINISHED'}<br><br>def menu_func_import(self, context):<br>    self.layout.operator(ImportNeuroForge3D.bl_idname, text="NeuroForge 3D (.stl)")<br><br>def register():<br>    bpy.utils.register_class(ImportNeuroForge3D)<br>    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)<br><br>def unregister():<br>    bpy.utils.unregister_class(ImportNeuroForge3D)<br>    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)<br>```<br>Testar no Blender 3.6+. | • Add-on pode ser instalado no Blender (Preferences > Add-ons)<br>• Opção "Import > NeuroForge 3D" aparece no menu File<br>• Importar STL via add-on funciona corretamente<br>• Mesh importada está visível na cena | **Usar Agentic Search para:**<br>- "Blender Python add-on template 2024"<br>- "Blender import STL programmatically bpy" |
| **S4-T05** | Adicionar Integração Direta Gradio → Blender | Criar funcionalidade para enviar modelo do Gradio direto pro Blender.<br><br>**Implementação:**<br>Em `gradio_app.py`:<br>```python<br>def generate_and_open_blender(prompt: str):<br>    output_path = generate_3d(prompt, "Trellis")<br>    # Gerar comando para Blender<br>    blender_cmd = f'blender --python -c "import bpy; bpy.ops.import_mesh.stl(filepath=\\"{output_path}\\")"'<br>    return output_path, blender_cmd<br>```<br>Adicionar botão "Open in Blender" na interface.<br>Documentar no README que Blender deve estar no PATH. | • Botão "Open in Blender" está visível<br>• Clicar no botão abre Blender com modelo carregado (se Blender estiver instalado)<br>• Mensagem de erro clara se Blender não estiver no PATH<br>• Funcionalidade é opcional (não quebra se Blender não disponível) | **Usar Agentic Search para:**<br>- "Open Blender from Python subprocess with model"<br>- "Blender command line import STL" |
| **S4-T06** | Criar Documentação de Uso | Criar `docs/USER_GUIDE.md` com instruções completas.<br><br>**Implementação:**<br>Incluir:<br>1. **Instalação:**<br>   - Requisitos de sistema (GPU, VRAM)<br>   - Instalação via Docker<br>   - Instalação local com venv<br>2. **Uso do Gradio:**<br>   - Como acessar interface<br>   - Como escrever bons prompts<br>   - Troubleshooting comum<br>3. **Uso do Blender Add-on:**<br>   - Como instalar<br>   - Como importar modelos<br>4. **Exemplos:**<br>   - Galeria de prompts e resultados | • `docs/USER_GUIDE.md` existe e está completo<br>• Seguir o guia do zero resulta em instalação funcional<br>• Screenshots/GIFs ilustram os passos (opcional)<br>• Seção de FAQ cobre erros comuns | Não requer Agentic Search |
| **S4-T07** | Criar Script de Deploy (Docker Compose) | Criar `docker-compose.yml` para deploy simplificado.<br><br>**Implementação:**<br>```yaml<br>version: '3.8'<br>services:<br>  neuroforge3d:<br>    build: .<br>    ports:<br>      - "7860:7860"<br>    volumes:<br>      - ./models:/app/models<br>      - ./outputs:/app/outputs<br>    deploy:<br>      resources:<br>        reservations:<br>          devices:<br>            - driver: nvidia<br>              count: 1<br>              capabilities: [gpu]<br>    environment:<br>      - GRADIO_SERVER_NAME=0.0.0.0<br>```<br>Adicionar script `start.sh` para facilitar. | • `docker-compose.yml` existe<br>• `docker-compose up` inicia aplicação com GPU<br>• Interface Gradio acessível em `http://localhost:7860`<br>• Volumes persistem modelos e outputs<br>• Script `start.sh` automatiza setup inicial | **Usar Agentic Search para:**<br>- "Docker Compose GPU support NVIDIA runtime 2024" |

---

## 📋 RESUMO DE DEPENDÊNCIAS ENTRE SPRINTS

```
Sprint 0 (Setup) ──┬─→ Sprint 1 (Infra) ──→ Sprint 2 (IA) ──┐
                   │                                         │
                   └─→ Sprint 3 (Processing) ←──────────────┤
                                    │                        │
                                    └────────→ Sprint 4 (UI) ←┘
```

**Regras:**
- Sprint 0 pode ser executado em paralelo com Sprint 1 (setup de CI não bloqueia código)
- Sprint 2 depende de Sprint 1 (precisa da estrutura base)
- Sprint 3 pode começar assim que BaseGenerator existir (S1-T03)
- Sprint 4 depende de S2 e S3 estarem completos

---

## 🚀 COMANDOS DE INICIALIZAÇÃO (Sprint 0 - Primeiros Passos)

Para começar imediatamente a trabalhar no projeto, execute os seguintes comandos no terminal:

### 1️⃣ Criar estrutura de diretórios e arquivos de workflow
```bash
mkdir -p .github/workflows .devcontainer docs scripts src/{core,processing,ui,utils} tests models outputs
touch .github/workflows/{gemini-review.yml,ci.yml,docker-build.yml}
touch .devcontainer/devcontainer.json
touch setup_env.sh
echo "models/*" >> .gitignore
echo "outputs/*" >> .gitignore
echo "!models/.gitkeep" >> .gitignore
echo "!outputs/.gitkeep" >> .gitignore
echo ".venv/" >> .gitignore
```

### 2️⃣ Criar ambiente virtual Python
```bash
python3 -m venv .venv
source .venv/bin/activate  # No Windows: .venv\Scripts\activate
pip install --upgrade pip
pip install black ruff pytest
```

### 3️⃣ Configurar Git e fazer primeiro commit
```bash
git config --global user.email "your-email@example.com"
git config --global user.name "Your Name"
git add .
git commit -m "chore: Initialize project structure for NeuroForge 3D"
```

---

## 📊 MÉTRICAS DE SUCESSO POR SPRINT

### Sprint 0
- [ ] CI/CD workflows funcionando
- [ ] Ambiente de desenvolvimento configurado
- [ ] Agentic Search testado e documentado

### Sprint 1
- [ ] Docker build < 8GB
- [ ] MockGenerator gera STL válido
- [ ] Estrutura de código passa no linting

### Sprint 2
- [ ] TrellisGenerator gera modelos 3D
- [ ] Gestão de VRAM funciona corretamente
- [ ] Tempo de inferência < 60s para modelos simples

### Sprint 3
- [ ] Pipeline repara 90%+ de meshes quebradas
- [ ] Normalização de escala ±1mm de precisão
- [ ] Validação detecta todos os casos inválidos

### Sprint 4
- [ ] Interface Gradio suporta 10+ usuários simultâneos
- [ ] Blender add-on instalável e funcional
- [ ] Documentação completa e testada

---

## 🔍 VERIFICAÇÃO FINAL (Antes do Release)

Antes de marcar qualquer sprint como "completo", execute esta checklist:

- [ ] **Código:** Passa em `ruff check src/ tests/`
- [ ] **Formatação:** Passa em `black --check src/ tests/`
- [ ] **Testes:** `pytest tests/` com cobertura > 70%
- [ ] **Docker:** Build sem erros e imagem < 8GB
- [ ] **CI:** Todos os workflows em verde no GitHub Actions
- [ ] **Documentação:** README.md atualizado com instruções de uso
- [ ] **Segurança:** Nenhuma credencial ou API key no código
- [ ] **Gemini Review:** PR foi revisado pelo Gemini Code Assist

---

## 📚 RECURSOS ADICIONAIS

### Documentação de Referência
- [Trimesh Documentation](https://trimsh.org/)
- [Gradio Documentation](https://gradio.app/docs/)
- [Blender Python API](https://docs.blender.org/api/current/)
- [HuggingFace Hub](https://huggingface.co/docs/hub/)

### Agentic Search - Quando Usar
Use **antes** de implementar:
- Novos modelos de IA (verificar versões e mudanças de API)
- Bibliotecas com atualizações frequentes (ex: Gradio, diffusers)
- Configurações de infra (Docker, CUDA, GitHub Actions)
- Práticas de segurança ou performance

---

**Versão:** 1.0  
**Última Atualização:** 2024-11  
**Status:** Ready for Implementation 🚀
