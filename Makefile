# Makefile for AI Dev Tool

.PHONY: help init install clean test format lint type-check run-test build docs

# Default target
help:
	@echo "AI Dev Tool - Makefile Commands"
	@echo "================================"
	@echo ""
	@echo "Setup & Installation:"
	@echo "  make init          - Complete initialization (venv, deps, config)"
	@echo "  make install       - Install dependencies only"
	@echo "  make install-dev   - Install with development dependencies"
	@echo ""
	@echo "Development:"
	@echo "  make test          - Run tests"
	@echo "  make format        - Format code with black"
	@echo "  make lint          - Lint code with ruff"
	@echo "  make type-check    - Type check with mypy"
	@echo "  make check         - Run all checks (format, lint, type-check)"
	@echo ""
	@echo "Utilities:"
	@echo "  make clean         - Clean temporary files and caches"
	@echo "  make clean-all     - Clean everything including venv"
	@echo "  make run-test      - Run a quick functionality test"
	@echo "  make build         - Build distribution packages"
	@echo ""
	@echo "AI Commands:"
	@echo "  make status        - Show tool status"
	@echo "  make sample        - Generate sample documents"
	@echo ""

# Complete initialization
init:
	@echo "Initializing AI Dev Tool..."
	@bash .init.sh

# Install dependencies
install:
	@echo "Installing dependencies..."
	@pip install --upgrade pip
	@pip install -r requirements.txt
	@pip install -e .

# Install with dev dependencies
install-dev:
	@echo "Installing dependencies with dev tools..."
	@pip install --upgrade pip
	@pip install -r requirements.txt
	@pip install -e ".[dev]"

# Run tests
test:
	@echo "Running tests..."
	@pytest tests/ -v

# Format code
format:
	@echo "Formatting code with black..."
	@black src/ tests/ --line-length 100

# Lint code
lint:
	@echo "Linting code with ruff..."
	@ruff check src/ tests/ --fix

# Type checking
type-check:
	@echo "Type checking with mypy..."
	@mypy src/

# Run all checks
check: format lint type-check
	@echo "All checks completed!"

# Clean temporary files
clean:
	@echo "Cleaning temporary files..."
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@find . -type f -name "*.pyo" -delete 2>/dev/null || true
	@find . -type f -name "*.pyd" -delete 2>/dev/null || true
	@find . -type f -name ".coverage" -delete 2>/dev/null || true
	@find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	@rm -rf build/ dist/ 2>/dev/null || true
	@echo "Cleanup completed!"

# Clean everything including venv
clean-all: clean
	@echo "Removing virtual environment..."
	@rm -rf venv/ 2>/dev/null || true
	@rm -rf output/ 2>/dev/null || true
	@rm -f sample_input*.txt 2>/dev/null || true
	@rm -f test_*.txt 2>/dev/null || true
	@echo "Full cleanup completed!"

# Build distribution packages
build: clean
	@echo "Building distribution packages..."
	@python -m build
	@echo "Build completed! Check dist/ directory"

# Run tool status
status:
	@echo "Checking AI Dev Tool status..."
	@ai-dev status

# Generate sample documents
sample:
	@echo "Generating sample documents..."
	@echo "Creating sample input file..."
	@echo "ユーザー認証システムの開発\n\n以下の機能が必要です：\n- メールとパスワードによるログイン\n- パスワードリセット機能\n- 2段階認証\n- セッション管理" > sample_test.txt
	@echo ""
	@echo "Generating requirements..."
	@ai-dev generate requirements sample_test.txt -o output/sample_requirements.md
	@echo ""
	@echo "Generating test cases..."
	@ai-dev generate test-cases sample_test.txt -o output/sample_tests.csv -f csv
	@echo ""
	@echo "Sample documents generated in output/ directory"
	@rm -f sample_test.txt

# Run a quick functionality test
run-test:
	@echo "Running functionality test..."
	@python -c "from ai_dev.cli import cli; print('✓ CLI import successful')"
	@python -c "from ai_dev.config import ConfigManager; print('✓ Config import successful')"
	@python -c "from ai_dev.generators import RequirementsGenerator; print('✓ Generators import successful')"
	@python -c "from ai_dev.utils import EncodingHandler; print('✓ Utils import successful')"
	@echo ""
	@ai-dev --version || ai-dev --help | head -n 1
	@echo ""
	@echo "✓ All imports successful!"

# Create directories
dirs:
	@mkdir -p src/ai_dev/{config,ai_models,generators,analyzers,prompts,templates,utils}
	@mkdir -p tests config templates output docs
	@echo "Directories created!"

# Development server (if web interface is added in future)
serve:
	@echo "Web interface not yet implemented"
	@echo "Use 'ai-dev' CLI commands instead"

# Watch for changes (for development)
watch:
	@echo "Watching for file changes..."
	@watchmedo auto-restart --directory=./src --pattern="*.py" --recursive -- ai-dev status

.PHONY: venv
venv:
	@if [ ! -d "venv" ]; then \
		echo "Creating virtual environment..."; \
		python3 -m venv venv; \
	fi
	@echo "Virtual environment ready. Activate with: source venv/bin/activate"