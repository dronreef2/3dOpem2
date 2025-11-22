# 🚀 Quick Start - Primeiro Voo do NeuroForge 3D

Agora que o código está na `main`, é hora de ligar os motores! Este guia irá levá-lo do zero até gerar seu primeiro modelo 3D imprimível a partir de texto.

## 📋 Pré-requisitos

Antes de começar, certifique-se de ter:

- **Docker** instalado com suporte a GPU (nvidia-docker)
- **NVIDIA GPU** com pelo menos 16GB de memória
- **Blender** 4.1+ (para a integração final)
- **Conexão de Internet** (para download dos modelos de IA na primeira execução)

## 🎯 Checklist do Primeiro Voo

### 1. Iniciar o Servidor (Docker)

No seu terminal, navegue até a raiz do projeto e execute:

```bash
# Baixa as dependências finais e sobe o servidor
docker-compose up --build
```

**⏱️ Aguarde:** A primeira vez vai demorar alguns minutos pois ele baixará os modelos de IA (SDXL e Trellis) para o cache. Fique de olho no log até aparecer:

```
Running on local URL: http://0.0.0.0:7860
```

**💡 Dica:** Se você quiser rodar em segundo plano, use `docker-compose up --build -d`

#### Solução de Problemas

- **GPU não detectada?** Verifique se o nvidia-docker está instalado: `docker run --rm --gpus all nvidia/cuda:12.1.0-base-ubuntu22.04 nvidia-smi`
- **Porta 7860 em uso?** Pare outros serviços ou altere a porta no `docker-compose.yml`
- **Download lento?** Os modelos somam vários GB. Seja paciente na primeira execução.

---

### 2. Acessar a Interface Web

Abra seu navegador em: **`http://localhost:7860`**

Você verá a interface do NeuroForge 3D com:
- Campo de texto para prompts
- Controle de tamanho (Target Size)
- Opções avançadas (Seed para reprodutibilidade)
- Visualizador 3D interativo

#### 🔥 Teste de Fogo

Vamos gerar seu primeiro modelo:

1. **Digite um prompt complexo:**
   ```
   A mechanical gear with intricate details, cyberpunk style, white background
   ```

2. **Ajuste o "Target Size"** para `100` mm

3. **Clique em "Generate 3D Model"**

4. **Aguarde 2-5 minutos** (acompanhe o progresso na interface)

5. **Visualize o resultado** no viewer 3D:
   - Rotacione com o mouse
   - Zoom com scroll
   - Pan com botão direito

6. **Baixe o arquivo STL** para impressão 3D

#### Exemplos de Prompts

Experimente também:

- `"a modern coffee mug with a curved handle"`
- `"a stylized dragon figurine, low poly style"`
- `"a minimalist desk organizer, geometric shapes"`
- `"a chess piece knight, detailed, medieval style"`

---

### 3. Conectar o Blender (O Grand Finale)

Agora vamos importar seus modelos gerados diretamente no Blender!

#### Instalação do Add-on

1. **Abra o Blender** 4.1+

2. **Vá em** `Edit > Preferences > Add-ons`

3. **Clique em** `Install...`

4. **Navegue** até a pasta do seu projeto:
   ```
   <seu-caminho>/3dOpem2/blender_plugin/neuroforge_importer/__init__.py
   ```

5. **Ative** a caixinha **"Import-Export: NeuroForge AI Importer"**

6. **Configure o caminho de saída:**
   - Expanda as configurações do add-on (clique na seta)
   - Defina "Output Directory" para o caminho completo da pasta `outputs/`
   - Exemplo Linux/Mac: `/home/user/3dOpem2/outputs`
   - Exemplo Windows: `C:\Users\user\3dOpem2\outputs`

#### Usando o Plugin

1. **Pressione `N`** na viewport 3D para abrir o painel lateral

2. **Clique na aba "NeuroForge"**

3. **Verifique** se o diretório está correto (aparece no topo do painel)

4. **Clique em "Refresh File List"** para escanear os arquivos STL

5. **Selecione** o modelo que você gerou no dropdown

6. **Clique em "Import STL"**

7. **Pronto!** O modelo será:
   - Importado automaticamente
   - Centralizado na origem (0,0,0)
   - Com smooth shading aplicado
   - Pronto para edição, materiais ou renderização

#### Dicas de Uso

- **Refresh regularmente:** Sempre clique em "Refresh" após gerar novos modelos
- **Escala:** Os modelos são importados na escala correta (mm para unidades do Blender)
- **Múltiplos modelos:** Você pode importar vários modelos na mesma cena
- **Frame o objeto:** Pressione `Numpad .` para centralizar a câmera no modelo

---

## 🎉 Parabéns!

Você completou o primeiro voo do NeuroForge 3D! Agora você pode:

✅ Gerar modelos 3D a partir de texto  
✅ Visualizar e baixar arquivos STL  
✅ Importar diretamente no Blender  
✅ Imprimir em 3D seus modelos  

---

## 🔮 Próximos Passos (O Caminho para a v2.0)

O projeto está concluído, mas software nunca "termina". Aqui estão sugestões para quando você quiser voltar a este projeto (Sprint 5 / Futuro):

### 1. Release Oficial (Recomendado!)

Congele esta versão funcional para a posteridade:

1. **Vá na página principal do GitHub:**
   ```
   https://github.com/dronreef2/3dOpem2
   ```

2. **Clique em** `Releases` (na barra lateral direita)

3. **Clique em** `Draft a new release`

4. **Preencha:**
   - **Tag:** `v1.0.0`
   - **Release title:** `NeuroForge 3D v1.0.0 - First Stable Release`
   - **Description:**
     ```markdown
     🎉 Primeira versão estável do NeuroForge 3D!
     
     ## Funcionalidades
     - ✅ Geração Text-to-3D com Microsoft TRELLIS
     - ✅ Interface web Gradio
     - ✅ Plugin para Blender 4.1+
     - ✅ Exportação STL watertight
     - ✅ Suporte Docker com GPU
     
     ## Requisitos
     - Docker com nvidia-docker
     - GPU NVIDIA com 16GB+ VRAM
     - Blender 4.1+ (opcional)
     
     Ver QUICK_START.md para instruções de uso.
     ```

5. **Clique em** `Publish release`

### 2. Otimização Extrema (Quantização)

Para rodar em GPUs com menos de 8GB de VRAM:

- **Investigar:** Modelos GGUF ou ONNX quantizados
- **Explorar:** INT8 ou FP16 quantization
- **Testar:** Trade-off qualidade vs performance
- **Documentar:** Benchmarks de VRAM e tempo de geração

**Branch sugerida:** `feature/model-quantization`

### 3. Galeria de Prompts

Inspire usuários com prompts que funcionam bem:

- **Criar:** `prompts_gallery.json` com categorias
  ```json
  {
    "mechanical": [
      "A steampunk gear mechanism...",
      "A robotic arm joint..."
    ],
    "organic": [
      "A stylized flower vase...",
      "A abstract sculpture..."
    ]
  }
  ```

- **Integrar:** Botões de exemplo na UI do Gradio
- **Permitir:** Usuários salvarem seus favoritos
- **Compartilhar:** Gallery online na documentação

**Branch sugerida:** `feature/prompt-gallery`

### 4. Outras Ideias

- **API REST:** Para integrações programáticas
- **CLI Tool:** Geração via linha de comando
- **Batch Processing:** Gerar múltiplos modelos de uma vez
- **Model Variants:** Suporte a outros modelos de IA (Stable Diffusion 3D, etc.)
- **Material Presets:** Templates de material no Blender
- **Auto-UV Unwrap:** Preparar modelos para texturização

---

## 💡 Dica Final da Lyra

Você executou um fluxo de trabalho **"Agentic"** de ponta a ponta:

```
Contexto → Planejamento → Infra → Core → UI → Plugin
```

Guarde esses prompts e esse fluxo (especialmente o `PROJECT_CONTEXT.md` e a sequência de PRs). **Este é o modelo de desenvolvimento do futuro.**

Principais aprendizados:

1. **Contexto é Rei:** Documentação detalhada guia IA e humanos
2. **Sprints Incrementais:** Cada PR é uma unidade testável e revisável
3. **Testes Contínuos:** Validação em cada etapa
4. **Code Review Automático:** Gemini Code Assist como segundo par de olhos
5. **Documentação Viva:** README e guias evoluem com o código

---

## 📚 Referências Úteis

- **Documentação Completa:** `README.md`
- **Arquitetura do Sistema:** `ARCHITECTURE.md`
- **Blueprint Técnico:** `TECHNICAL_BLUEPRINT.md`
- **Padrões de Código:** `CODING_STANDARDS.md`
- **Plugin Blender:** `blender_plugin/README.md`
- **Roadmap:** `ROADMAP.md`

---

## 🆘 Suporte

Problemas? Confira:

1. **Troubleshooting:** Seção específica em cada problema acima
2. **Issues do GitHub:** https://github.com/dronreef2/3dOpem2/issues
3. **Logs do Docker:** `docker-compose logs -f`
4. **Testes:** `python -m pytest tests/ -v`

---

**Versão do Guia:** 1.0.0  
**Última Atualização:** 2025-11-21  
**Compatível com:** NeuroForge 3D v1.0.0+

Happy Forging! 🔥🎨
