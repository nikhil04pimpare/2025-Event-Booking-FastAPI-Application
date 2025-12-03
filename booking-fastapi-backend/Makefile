.PHONY: help install format lint type-check test clean pre-commit-install pre-commit-run

help:
	@echo "Available commands:"
	@echo "  make install              - Install project dependencies"
	@echo "  make format               - Format code with Black and isort"
	@echo "  make lint                 - Run Ruff linter"
	@echo "  make type-check           - Run Mypy type checker"
	@echo "  make quality              - Run all quality checks (format + lint + type-check)"
	@echo "  make test                 - Run tests with pytest"
	@echo "  make clean                - Remove cache and build files"
	@echo "  make pre-commit-install   - Install pre-commit hooks"
	@echo "  make pre-commit-run       - Run pre-commit on all files"

install:
	pip install -e .
	pip install black isort ruff mypy pytest bandit

format:
	black .
	isort .

lint:
	ruff check . --fix

type-check:
	mypy .

quality: format lint type-check
	@echo "✅ All quality checks passed!"

test:
	pytest -v

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +

pre-commit-install:
	pre-commit install

pre-commit-run:
	pre-commit run --all-files

dev: install pre-commit-install
	@echo "✅ Development environment setup complete!"
