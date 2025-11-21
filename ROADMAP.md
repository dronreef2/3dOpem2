# ROTEIRO DE DESENVOLVIMENTO (SPRINTS)

## 🛠️ SPRINT 0: CONFIGURAÇÃO DO AGENTE (IMEDIATO)
- [ ] Criar arquivo de workflow `.github/workflows/gemini-review.yml` (ou similar) para ativar o Gemini Code Assist nos PRs.
- [ ] Testar o "Agentic Search" pedindo para ele resumir a documentação atual do repositório `microsoft/TRELLIS`.
- [ ] Criar os arquivos de contexto (`PROJECT_CONTEXT.md`, `CODING_STANDARDS.md`).

## 🏁 SPRINT 1: INFRAESTRUTURA (Foco: Docker & Mock)
- [ ] Criar `Dockerfile` otimizado.
- [ ] Criar `requirements.txt`.
- [ ] Implementar `src/core/generator.py` (Mock Class).
- [ ] Configurar GitHub Action para buildar o container automaticamente ao receber push.

## 🧠 SPRINT 2: INTEGRAÇÃO DE IA
- [ ] Implementar `TrellisGenerator`.
- [ ] Script de download de pesos.

## ⚙️ SPRINT 3: PROCESSAMENTO 3D
- [ ] Pipeline de limpeza de malha (Trimesh).
- [ ] Validação de Manifold.

## 🖥️ SPRINT 4: UI & BLENDER
- [ ] Gradio App.
- [ ] Blender Add-on.
