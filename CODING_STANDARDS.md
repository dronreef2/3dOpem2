# AI AGENT CODING STANDARDS

## 1. OTIMIZAÇÃO PARA GEMINI CODE ASSIST
- **Contexto:** Adicione docstrings detalhadas explicando *o propósito* da função. Isso ajuda o Gemini a entender se a lógica corresponde à intenção durante o Code Review.
- **Complexidade:** Mantenha a complexidade ciclomática baixa. O Gemini sinalizará funções muito aninhadas.

## 2. ESTILO PYTHON
- Use Type Hinting sempre (`def func(a: int) -> str:`).
- Siga PEP 8.
- Use `pathlib` em vez de strings para caminhos de arquivo.

## 3. INFRAESTRUTURA
- Dependências estritas no `requirements.txt`.
- Logs devem usar a lib `logging`, nunca `print()`.
