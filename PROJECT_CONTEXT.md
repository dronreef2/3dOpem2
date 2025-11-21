# PROJECT CONTEXT: NeuroForge 3D

## MISSÃO DO PROJETO
Sistema "Text-to-Printable-3D" open-source. Foco em geometria válida para impressão (watertight STLs) usando Trellis/Hunyuan3D.

## STACK DE DESENVOLVIMENTO (AGENTIC TOOLS INSTALADAS)
Este repositório utiliza um pipeline de IA integrado. O Agente deve estar ciente das seguintes ferramentas disponíveis:
1.  **Gemini Code Assist:** Utilizado para Code Review em Pull Requests. O código gerado deve ser limpo o suficiente para passar na revisão automática do Gemini.
2.  **Agentic Search AI:** Disponível para pesquisar documentações recentes (ex: atualizações do Trimesh ou Trellis) antes de gerar código.
3.  **GitHub Actions:** CI/CD automatizado.

## ARQUITETURA TÉCNICA (RUNTIME)
1.  **Core AI:** Microsoft TRELLIS (Principal) ou Hunyuan3D-2.
2.  **Processamento:** `Trimesh` (foco em `is_watertight` e `repair`).
3.  **Infra:** Docker (`nvidia/cuda:12.1`).
4.  **Interface:** Gradio + Blender Add-on.

## REGRAS DE INTERAÇÃO
- **Pesquisa Antes de Codificar:** Use a capacidade de busca para verificar se métodos de bibliotecas (como `diffusers`) não foram depreciados.
- **Modo PR:** Todo código complexo deve ser planejado para ser submetido via Pull Request para análise do Gemini Code Assist.
