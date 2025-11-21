# AI AGENT CODING STANDARDS

## 1. ESTILO DE CÓDIGO (PYTHON)
- **Type Hinting:** OBRIGATÓRIO em todas as definições de função (ex: `def process(mesh: trimesh.Trimesh) -> str:`).
- **Docstrings:** Estilo Google. Descreva Args e Returns.
- **Modularidade:** Funções não devem exceder 50 linhas. Quebre lógica complexa em sub-helpers.
- **Imports:** Use caminhos absolutos (`from src.core.generator import ...`) em vez de relativos.

## 2. TRATAMENTO DE ERROS
- Nunca deixe um `try/except` vazio. Logue o erro usando `logging`.
- Para falhas na geração de IA, implemente um retry (máximo 3 tentativas) antes de falhar.

## 3. GERENCIAMENTO DE DEPENDÊNCIAS
- Não instale pacotes via `os.system('pip install')` dentro do código Python.
- Todas as dependências devem estar listadas no `requirements.txt`.
- Use versões fixas para libs críticas (torch, trimesh, numpy).

## 4. REGRAS ESPECÍFICAS DE 3D
- **Eixo Z:** Assuma Z-up (padrão Blender/Impressão 3D).
- **Unidades:** Trabalhe internamente em milímetros (mm).
- **Logs:** Logue as dimensões do bounding box final para debug.
