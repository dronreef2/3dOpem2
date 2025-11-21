# PROJECT CONTEXT: NeuroForge 3D

## MISSÃO DO PROJETO
Desenvolver um sistema "Text-to-Printable-3D" open-source e de baixo custo. O objetivo não é apenas gerar visualizações 3D, mas sim arquivos .STL otimizados, "watertight" (fechados) e prontos para fatiadores (slicers) de impressão 3D.

## ARQUITETURA TÉCNICA (IMUTÁVEL)
1.  **Core AI:** Microsoft TRELLIS (Preferencial) ou Hunyuan3D-2.
    *   *Fallback:* Shap-E (apenas se VRAM < 8GB).
2.  **Processamento de Malha:** `Trimesh` e `PyMeshLab`.
    *   *Regra:* Toda malha deve passar por verificação de `is_watertight` antes de ser salva.
3.  **Interface:** Gradio (Web UI).
4.  **Infraestrutura:** Docker (Base: `nvidia/cuda:12.1-devel-ubuntu22.04`).
5.  **Integração Externa:** Blender Add-on (monitora pasta de saída).

## RESTRIÇÕES DE HARDWARE
O código deve ser otimizado para rodar em GPUs de consumo (RTX 3060/4060).
- Use `torch.float16` sempre que possível.
- Implemente `cpu_offload` para os modelos.

## ESTRUTURA DE DIRETÓRIOS ALVO
/src
  /core (Lógica da IA)
  /processing (Lógica de geometria/trimesh)
  /ui (Gradio)
/blender_plugin (Add-on)
/output (Volume compartilhado)
