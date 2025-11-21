# NeuroForge 3D

Sistema "Text-to-Printable-3D" open-source focado em geometria válida para impressão 3D (watertight STLs) usando Microsoft TRELLIS.

## 📋 Visão Geral

NeuroForge 3D é um projeto que utiliza modelos de IA de última geração para gerar modelos 3D imprimíveis a partir de texto ou imagens. O sistema é construído sobre o [Microsoft TRELLIS](https://github.com/microsoft/TRELLIS), uma solução state-of-the-art para geração 3D, com foco especial em garantir que os modelos gerados sejam watertight (fechados) e prontos para impressão 3D.

## 🛠️ Stack Tecnológica

- **Core AI:** Microsoft TRELLIS
- **Processamento 3D:** Trimesh (foco em `is_watertight` e `repair`)
- **Infraestrutura:** Docker com NVIDIA CUDA 12.1
- **Interface:** Gradio + Blender Add-on (futuro)
- **Python:** 3.10+
- **PyTorch:** 2.4.0 com CUDA 12.1

## 🚀 Quick Start

### Pré-requisitos

- Docker com suporte a GPU (nvidia-docker)
- NVIDIA GPU com pelo menos 16GB de memória
- CUDA Toolkit 12.1 ou superior

### Instalação com Docker

1. Clone o repositório:
```bash
git clone https://github.com/dronreef2/3dOpem2.git
cd 3dOpem2
```

2. Construa a imagem Docker:
```bash
docker build -t neuroforge3d:latest .
```

3. Execute o container:
```bash
docker run --gpus all -it --rm \
  -v $(pwd):/app \
  -p 7860:7860 \
  neuroforge3d:latest
```

### Instalação Local (Alternativa)

1. Crie um ambiente virtual:
```bash
python3.10 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

2. Instale PyTorch com CUDA 12.1:
```bash
pip install torch==2.4.0 torchvision==0.19.0 --index-url https://download.pytorch.org/whl/cu121
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Instale xformers:
```bash
pip install xformers==0.0.27.post2 --index-url https://download.pytorch.org/whl/cu121
```

## 🎯 Quick Start (Local Testing)

Para testar rapidamente o sistema sem Docker:

```bash
# Instalar apenas dependências básicas para teste
pip install trimesh scipy numpy pytest

# Rodar demo para ver o sistema em ação
python demo.py

# Rodar testes
python -m pytest tests/ -v
```

Isto irá gerar arquivos STL de teste na pasta `outputs/` demonstrando:
- Geração de malhas com validação watertight
- Pipeline de processamento (reparo, escala, validação)
- Diferentes formas geométricas (box, sphere, cylinder)

## 📦 Dependências Principais

- **PyTorch 2.4.0** com CUDA 12.1
- **Trimesh** - Processamento e validação de malhas 3D
- **Open3D** - Visualização e processamento de nuvens de pontos
- **Transformers** - Modelos de linguagem e visão
- **Gradio** - Interface web
- **xformers** - Mecanismos de atenção otimizados

Ver `requirements.txt` para lista completa.

## 🎨 Usando a Interface Web (Gradio)

### Iniciar a Interface

**Com Docker Compose (Recomendado):**
```bash
docker-compose up
# Acesse http://localhost:7860 no navegador
```

**Com Docker Run:**
```bash
docker run --gpus all -p 7860:7860 -v $(pwd)/outputs:/app/outputs neuroforge3d:latest python launch_ui.py
```

**Localmente:**
```bash
python launch_ui.py
# ou
python -m src.ui.app
```

### Usando a Interface

1. **Abra seu navegador** em `http://localhost:7860`
2. **Digite um prompt** descrevendo o modelo 3D desejado
   - Exemplo: "a modern coffee mug with a curved handle"
3. **Configure os parâmetros:**
   - **Target Size**: Tamanho em mm (10-500mm)
   - **Seed**: Para resultados reproduzíveis (opcional)
4. **Clique em "Generate 3D Model"**
5. **Aguarde** a geração (2-5 minutos)
6. **Visualize** o modelo 3D no viewer interativo
7. **Download** o arquivo STL para impressão 3D

### Recursos da Interface

- ✅ **Visualização 3D Interativa**: Rotacione e examine o modelo
- ✅ **Download Direto**: Baixe o STL pronto para impressão
- ✅ **Exemplos**: Prompts prontos para experimentar
- ✅ **Queue System**: Gerencia requisições longas sem timeout
- ✅ **Feedback em Tempo Real**: Acompanhe o progresso da geração

## 🔧 Plugin para Blender

### Instalação

1. **Abra o Blender** (versão 3.0+)
2. **Vá em** `Edit > Preferences > Add-ons`
3. **Clique em** `Install...`
4. **Selecione** `blender_plugin/neuroforge_importer/__init__.py`
5. **Ative** o add-on "NeuroForge 3D Importer"
6. **Configure** o diretório de output nas preferências do add-on

### Configuração com Docker

Se você usa Docker, mapeie o volume de outputs:

```bash
# Docker Compose (já configurado)
docker-compose up

# Ou com docker run
docker run --gpus all -v $(pwd)/outputs:/app/outputs -p 7860:7860 neuroforge3d:latest
```

No Blender, configure o caminho local do diretório `outputs` nas preferências do add-on.

### Uso do Plugin

1. **Abra o painel** pressionando `N` na viewport 3D
2. **Clique na aba** "NeuroForge"
3. **Clique em "Refresh"** para listar os arquivos STL disponíveis
4. **Selecione um arquivo** no dropdown
5. **Clique em "Import STL"**
6. O modelo será importado, centralizado e com smooth shading aplicado!

### Recursos do Plugin

- 🔄 **Auto-refresh**: Lista todos os STLs do diretório
- 📦 **Import Inteligente**: Centraliza automaticamente
- 🎨 **Smooth Shading**: Aplica sombreamento suave
- ⚙️ **Configurável**: Define o diretório de outputs

Ver documentação completa em [`blender_plugin/README.md`](blender_plugin/README.md).

## 🗂️ Estrutura do Projeto

```
3dOpem2/
├── src/
│   ├── core/
│   │   ├── base_generator.py      # Abstract base class
│   │   ├── mock_generator.py      # Mock implementation
│   │   └── trellis_generator.py   # TRELLIS AI generator
│   ├── processing/
│   │   ├── mesh_repair.py         # Mesh repair utilities
│   │   ├── mesh_scaling.py        # Scaling utilities
│   │   ├── mesh_validator.py      # Validation utilities
│   │   └── pipeline.py            # Complete processing pipeline
│   ├── ui/
│   │   ├── __init__.py
│   │   └── app.py                 # Gradio web interface
│   └── utils/
├── blender_plugin/
│   └── neuroforge_importer/       # Blender add-on
│       └── __init__.py
├── models/                         # Pesos dos modelos (não versionados)
├── outputs/                        # Resultados gerados
├── tests/
├── Dockerfile
├── docker-compose.yml
├── launch_ui.py                    # Script para iniciar Gradio UI
├── requirements.txt
└── README.md
```

## 🏃 Roadmap de Desenvolvimento

### ✅ SPRINT 0: Configuração (Concluído)
- [x] Arquivos de contexto do projeto
- [x] Padrões de código

### ✅ SPRINT 1: Infraestrutura (Completo)
- [x] Criar `Dockerfile` otimizado
- [x] Criar `requirements.txt`
- [x] Implementar `src/core/base_generator.py` (Abstract Base Class)
- [x] Implementar `src/core/mock_generator.py` (Mock Class com validação watertight)
- [x] Criar estrutura de projeto completa
- [x] Implementar pipeline de processamento 3D
- [ ] Configurar GitHub Action para build automático

### 📅 SPRINT 2: Integração de IA
- [ ] Implementar `TrellisGenerator`
- [ ] Script de download de pesos

### ✅ SPRINT 3: Processamento 3D (Completo)
- [x] Pipeline de limpeza de malha (Trimesh)
- [x] Validação de Manifold com `mesh.is_watertight`
- [x] Normalização de escala
- [x] Sistema completo de reparo de malhas

### ✅ SPRINT 4: UI & Blender (Completo)
- [x] Gradio App
- [x] Blender Add-on

## 🔧 Ferramentas de Desenvolvimento

- **Gemini Code Assist:** Revisão automática de código em Pull Requests
- **Agentic Search AI:** Pesquisa de documentações atualizadas
- **GitHub Actions:** CI/CD automatizado

## 📝 Contribuindo

Este é um projeto open-source. Para contribuir:

1. Fork o repositório
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request (será revisado pelo Gemini Code Assist)

## 📄 Licença

Este projeto está sob a licença MIT. Ver arquivo `LICENSE` para mais detalhes.

## 🙏 Agradecimentos

- [Microsoft TRELLIS](https://github.com/microsoft/TRELLIS) - Core AI para geração 3D
- Comunidade open-source de ferramentas 3D

## 📧 Contato

Para questões e suporte, abra uma issue no GitHub.

---

**Nota:** Este projeto está em desenvolvimento ativo. A API e estrutura podem mudar frequentemente durante as primeiras sprints.
