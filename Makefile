# NeuroForge 3D - Makefile
# Facilita tarefas comuns de desenvolvimento

.PHONY: help setup install install-dev test clean docker-build docker-up docker-down validate demo ui

# Cores para output
GREEN := \033[0;32m
YELLOW := \033[1;33m
NC := \033[0m

help: ## Mostra esta mensagem de ajuda
	@echo "NeuroForge 3D - Comandos Disponíveis:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-15s$(NC) %s\n", $$1, $$2}'
	@echo ""

setup: ## Configura o projeto (cria diretórios, venv)
	@echo "$(GREEN)Configurando projeto...$(NC)"
	@./setup.sh

install: ## Instala dependências básicas
	@echo "$(GREEN)Instalando dependências básicas...$(NC)"
	pip install --upgrade pip
	pip install trimesh scipy numpy pillow pytest

install-dev: ## Instala todas as dependências (desenvolvimento)
	@echo "$(GREEN)Instalando todas as dependências...$(NC)"
	pip install --upgrade pip
	pip install -r requirements.txt
	@echo "$(YELLOW)Nota: PyTorch e xformers devem ser instalados separadamente para CUDA$(NC)"

test: ## Executa testes
	@echo "$(GREEN)Executando testes...$(NC)"
	python -m pytest tests/ -v

test-cov: ## Executa testes com cobertura
	@echo "$(GREEN)Executando testes com cobertura...$(NC)"
	python -m pytest tests/ --cov=src --cov-report=html --cov-report=term

validate: ## Valida estrutura do projeto
	@echo "$(GREEN)Validando projeto...$(NC)"
	python3 validate_project.py

demo: ## Executa demo script
	@echo "$(GREEN)Executando demo...$(NC)"
	python demo.py

ui: ## Inicia interface web Gradio
	@echo "$(GREEN)Iniciando interface web...$(NC)"
	python launch_ui.py

docker-build: ## Constrói imagem Docker
	@echo "$(GREEN)Construindo imagem Docker...$(NC)"
	docker-compose build

docker-up: ## Inicia containers Docker
	@echo "$(GREEN)Iniciando containers...$(NC)"
	docker-compose up

docker-down: ## Para containers Docker
	@echo "$(GREEN)Parando containers...$(NC)"
	docker-compose down

docker-logs: ## Mostra logs dos containers
	@docker-compose logs -f

docker-shell: ## Abre shell no container
	@docker-compose exec neuroforge3d bash

clean: ## Remove arquivos temporários e cache
	@echo "$(GREEN)Limpando arquivos temporários...$(NC)"
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	rm -rf htmlcov/ .coverage
	@echo "$(GREEN)Limpeza concluída!$(NC)"

clean-all: clean ## Remove tudo (incluindo outputs, models, venv)
	@echo "$(YELLOW)ATENÇÃO: Isso removerá outputs, models e venv!$(NC)"
	@read -p "Tem certeza? [y/N] " -n 1 -r; \
	echo; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		rm -rf outputs/ models/ logs/ tmp/ venv/; \
		echo "$(GREEN)Limpeza completa concluída!$(NC)"; \
	else \
		echo "$(YELLOW)Cancelado.$(NC)"; \
	fi

format: ## Formata código com black
	@echo "$(GREEN)Formatando código...$(NC)"
	black src/ tests/ *.py --exclude='/(venv)/'

lint: ## Executa linting com flake8
	@echo "$(GREEN)Executando linting...$(NC)"
	flake8 src/ tests/ --max-line-length=100 --exclude=venv

docs: ## Gera documentação
	@echo "$(GREEN)Documentação disponível em:$(NC)"
	@echo "  - README.md"
	@echo "  - QUICK_START.md"
	@echo "  - PROJECT_ORGANIZATION.md"
	@echo "  - ARCHITECTURE.md"
	@echo "  - TECHNICAL_BLUEPRINT.md"

status: ## Mostra status do projeto
	@echo "$(GREEN)Status do NeuroForge 3D:$(NC)"
	@echo ""
	@python3 validate_project.py

# Atalhos úteis
dev: install-dev validate ## Setup completo para desenvolvimento
quick: setup install demo ## Quick start: setup + install + demo
all: setup install-dev test validate ## Faz tudo: setup, install, test, validate
