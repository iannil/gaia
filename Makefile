# Makefile for GAIA Framework

.PHONY: help install test lint format clean docs

help:  ## 显示帮助信息
	@echo "GAIA Framework - 可用命令:"
	@echo ""
	@echo "  make install    - 安装包"
	@echo "  make dev        - 安装开发依赖"
	@echo "  make test       - 运行测试"
	@echo "  make lint       - 代码检查"
	@echo "  make format     - 代码格式化"
	@echo "  make docs       - 生成文档"
	@echo "  make clean      - 清理临时文件"
	@echo ""

install:  ## 安装包
	@echo "Installing GAIA Framework..."
	pip install -e .

dev:  ## 安装开发依赖
	@echo "Installing development dependencies..."
	pip install -e ".[dev,web]"

test:  ## 运行测试
	@echo "Running tests..."
	pytest tests/ -v --cov=gaia_core --cov=gaia_skills --cov=gaia_knowledge

test-verbose:  ## 详细测试输出
	@echo "Running tests with verbose output..."
	pytest tests/ -v -s --cov=gaia_core --cov=gaia_skills --cov=gaia_knowledge --cov-report=html

lint:  ## 代码检查
	@echo "Running linters..."
	@echo "Checking with ruff..."
	ruff check .
	@echo "Type checking with mypy..."
	mypy gaia_core/ gaia_skills/ gaia_knowledge/ --ignore-missing-imports

format:  ## 代码格式化
	@echo "Formatting code..."
	black gaia_core/ gaia_skills/ gaia_knowledge/ gaia_templates/ gaia_workflow/ gaia_integration/ gaia_cli/
	ruff check --fix .

format-check:  ## 检查格式
	@echo "Checking code format..."
	black --check gaia_core/ gaia_skills/ gaia_knowledge/ gaia_templates/ gaia_workflow/ gaia_integration/ gaia_cli/
	ruff check .

docs:  ## 生成文档
	@echo "Generating documentation..."
	@echo "Documentation available in docs/ directory"

clean:  ## 清理临时文件
	@echo "Cleaning up..."
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
	rm -rf .coverage htmlcov/ .tox/
	@echo "Clean complete"

run-api:  ## 启动 Web API
	@echo "Starting GAIA Web API..."
	uvicorn gaia_web.backend:app --reload --host 0.0.0.0 --port 8000

import-test:  ## 测试导入
	@echo "Testing imports..."
	python3 -c "from gaia_core import GAIAEngine; from gaia_skills import SkillManager; from gaia_knowledge import KnowledgeGraph; from gaia_templates import TemplateEngine; from gaia_workflow import WorkflowExecutor; print('All imports successful!')"

.PHONY: install dev test test-verbose lint format format-check docs clean run-api import-test
