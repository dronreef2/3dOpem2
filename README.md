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
docker build -t neuroforge3d:sprint1 .
```

3. Execute o container:
```bash
docker run --gpus all -it --rm \
  -v $(pwd):/app \
  -p 7860:7860 \
  neuroforge3d:sprint1
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

## 📦 Dependências Principais

- **PyTorch 2.4.0** com CUDA 12.1
- **Trimesh** - Processamento e validação de malhas 3D
- **Open3D** - Visualização e processamento de nuvens de pontos
- **Transformers** - Modelos de linguagem e visão
- **Gradio** - Interface web
- **xformers** - Mecanismos de atenção otimizados

Ver `requirements.txt` para lista completa.

## 🗂️ Estrutura do Projeto (Planejada)

```
3dOpem2/
├── src/
│   ├── core/
│   │   └── generator.py      # Interface principal de geração
│   ├── processors/
│   │   └── mesh_cleaner.py   # Pipeline de limpeza de malha
│   └── utils/
├── models/                    # Pesos dos modelos (não versionados)
├── outputs/                   # Resultados gerados
├── tests/
├── Dockerfile
├── requirements.txt
└── README.md
```

## 🏃 Roadmap de Desenvolvimento

### ✅ SPRINT 0: Configuração (Concluído)
- [x] Arquivos de contexto do projeto
- [x] Padrões de código

### 🚧 SPRINT 1: Infraestrutura (Em Andamento)
- [x] Criar `Dockerfile` otimizado
- [x] Criar `requirements.txt`
- [ ] Implementar `src/core/generator.py` (Mock Class)
- [ ] Configurar GitHub Action para build automático

### 📅 SPRINT 2: Integração de IA
- [ ] Implementar `TrellisGenerator`
- [ ] Script de download de pesos

### 📅 SPRINT 3: Processamento 3D
- [ ] Pipeline de limpeza de malha (Trimesh)
- [ ] Validação de Manifold

### 📅 SPRINT 4: UI & Blender
- [ ] Gradio App
- [ ] Blender Add-on

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
