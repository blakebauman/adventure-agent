# Linter Setup and Recommendations

## Current Setup

This project uses **Ruff** as the primary linter and formatter. Ruff is a fast, modern Python linter written in Rust that replaces multiple tools (flake8, isort, pyupgrade, etc.).

## Configuration

The linter is configured in `pyproject.toml`:

```toml
[tool.ruff]
lint.select = [
    "E",    # pycodestyle errors
    "F",    # pyflakes
    "I",    # isort (import sorting)
    "D",    # pydocstyle
    "D401", # First line should be in imperative mood
    "T201", # Print statements (enabled but ignored - see below)
    "UP",   # pyupgrade (modern Python syntax)
]
lint.ignore = [
    "UP006",  # Allow typing.List, typing.Dict (for compatibility)
    "UP007",  # Allow typing.Union (for compatibility)
    "UP035",  # Allow typing_extensions imports
    "D417",   # Relax docstring parameter documentation
    "E501",   # Line length (handled by formatter)
    "T201",   # Print statements (used for error logging)
]
[tool.ruff.lint.per-file-ignores]
"tests/*" = ["D", "UP"]  # Relaxed rules for tests
"src/agent/graph.py" = ["E402"]  # Conditional imports are intentional
```

## Usage

### Check for Issues
```bash
ruff check src/
```

### Auto-fix Issues
```bash
ruff check --fix src/
```

### Format Code
```bash
ruff format src/
```

### Check and Format (Recommended)
```bash
ruff check --fix src/ && ruff format src/
```

## Pre-commit Hook (Recommended)

To automatically run linting before commits, add a pre-commit hook:

1. Install pre-commit:
```bash
uv pip install pre-commit
```

2. Create `.pre-commit-config.yaml`:
```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.8.2
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
```

3. Install the hook:
```bash
pre-commit install
```

## IDE Integration

### VS Code / Cursor
Install the "Ruff" extension. It will automatically use the configuration from `pyproject.toml`.

### PyCharm
1. Install the Ruff plugin
2. Configure it to use the project's Ruff installation
3. Enable "Run Ruff on save"

## Common Issues and Solutions

### Print Statements (T201)
Print statements are ignored because they're used for error logging in exception handlers. For production code, consider using Python's `logging` module instead:

```python
import logging
logger = logging.getLogger(__name__)

# Instead of: print(f"Error: {e}")
logger.error(f"Error: {e}")
```

### Import Sorting (I001)
Ruff automatically sorts imports. Run `ruff check --fix` to fix import order.

### Type Annotations (UP045)
Ruff suggests using modern `X | None` syntax instead of `Optional[X]`. This is auto-fixable with `--fix`.

### Unused Imports (F401)
Ruff automatically removes unused imports with `--fix`.

## Continuous Integration

Add linting to your CI/CD pipeline:

```yaml
# Example GitHub Actions
- name: Lint with Ruff
  run: |
    ruff check src/
    ruff format --check src/
```

## Additional Tools

### Type Checking
This project also uses **MyPy** for static type checking:

```bash
mypy src/
```

### Testing
Use **Pytest** for running tests:

```bash
pytest tests/
```

## Summary

- ✅ **Ruff** is configured and working
- ✅ All linting issues have been resolved
- ✅ Auto-fixable issues are handled automatically
- ✅ Print statements are allowed for error logging
- ✅ Conditional imports in `graph.py` are allowed

## Next Steps

1. Set up pre-commit hooks for automatic linting
2. Consider replacing `print()` statements with proper logging
3. Add linting to CI/CD pipeline
4. Run `ruff check --fix src/` regularly during development

