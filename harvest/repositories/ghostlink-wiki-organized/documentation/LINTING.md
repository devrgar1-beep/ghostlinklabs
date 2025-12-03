# Linting and Code Correction

GhostLink includes comprehensive linting and code correction tools.

## Tools Configured

- **Black**: Code formatter (100 char line length)
- **Ruff**: Fast Python linter with auto-fix
- **mypy**: Static type checker
- **pre-commit**: Git hooks for automatic checks

## Quick Start

```bash
# Install dev dependencies
make install-dev
# or
pip install -e ".[dev]"

# Format code
make format

# Run linters
make lint

# Check without modifying
make check

# Run tests
make test

# Auto-fix all issues
make fix
```

## VS Code Integration

VS Code is configured to automatically:
- Format on save using Black
- Fix issues on save using Ruff
- Organize imports on save
- Show linting errors inline

## Pre-commit Hooks

Install git hooks to check code before committing:

```bash
pip install pre-commit
pre-commit install
```

This will automatically:
- Format code with Black
- Lint and fix with Ruff
- Type check with mypy
- Check for common issues (trailing whitespace, large files, etc.)

## Manual Commands

```bash
# Format all code
black ghostlink/

# Lint with Ruff
ruff check ghostlink/

# Auto-fix with Ruff
ruff check --fix ghostlink/

# Type check with mypy
mypy ghostlink/

# Run pre-commit on all files
pre-commit run --all-files
```

## Ruff Rules

Enabled rules:
- **E, W**: pycodestyle errors and warnings
- **F**: pyflakes (unused imports, undefined names)
- **I**: isort (import sorting)
- **N**: PEP8 naming conventions
- **UP**: pyupgrade (modern Python syntax)
- **B**: flake8-bugbear (common bugs)
- **C4**: flake8-comprehensions (better comprehensions)
- **SIM**: flake8-simplify (code simplification)
- **TCH**: flake8-type-checking (type checking imports)
- **PTH**: flake8-use-pathlib (pathlib usage)
- **RET**: flake8-return (return statements)
- **TID**: flake8-tidy-imports (import hygiene)

## Configuration Files

- `pyproject.toml`: Main configuration for Black, Ruff, mypy, pytest
- `.pre-commit-config.yaml`: Pre-commit hook configuration
- `.vscode/settings.json`: VS Code editor settings
- `Makefile`: Quick commands for common tasks
