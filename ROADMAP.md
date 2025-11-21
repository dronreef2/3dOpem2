# ROTEIRO DE DESENVOLVIMENTO (SPRINTS)

Use este arquivo para entender a prioridade atual. Não execute tarefas de sprints futuros sem permissão explicita.

## 🏁 SPRINT 1: INFRAESTRUTURA (ATUAL)
- [ ] Criar `Dockerfile` otimizado (CUDA 12.1).
- [ ] Criar `requirements.txt` com versões travadas.
- [ ] Implementar `src/core/generator.py` com classe Mock (retorna cubo simples para teste).
- [ ] Script de teste `tests/test_infra.py` para validar ambiente GPU.

## 🧠 SPRINT 2: INTEGRAÇÃO DE IA (PENDENTE)
- [ ] Implementar `TrellisGenerator` real.
- [ ] Script de download automático de pesos (`scripts/download_weights.py`).
- [ ] Otimização de VRAM (float16).

## ⚙️ SPRINT 3: PROCESSAMENTO DE MALHA (PENDENTE)
- [ ] Implementar `src/processing/slicer_prep.py`.
- [ ] Função de reparo automático (Manifold).
- [ ] Função de auto-scaling (100mm).

## 🖥️ SPRINT 4: INTERFACE (PENDENTE)
- [ ] App Gradio com visualizador 3D.
- [ ] Add-on do Blender funcional.
