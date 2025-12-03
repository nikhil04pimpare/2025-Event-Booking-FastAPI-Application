# Quick Start Guide

## Development Tools Setup

### Initial Setup

**On Linux/macOS:**
```bash
make dev
```

**On Windows:**
```bash
.\dev.bat dev
```

This installs all dependencies and pre-commit hooks automatically.

## Common Commands

### Format & Lint Code

**Check what needs fixing:**
```bash
# Linux/macOS
make quality

# Windows
.\dev.bat quality
```

**Just format code:**
```bash
# Linux/macOS
make format

# Windows
.\dev.bat format
```

**Just run linter:**
```bash
# Linux/macOS
make lint

# Windows
.\dev.bat lint
```

### Run Tests

```bash
# Linux/macOS
make test

# Windows
.\dev.bat test
```

### Clean Cache

```bash
# Linux/macOS
make clean

# Windows
.\dev.bat clean
```

## Git Workflow

1. **Before committing**, run quality checks:
   ```bash
   # Linux/macOS
   make quality

   # Windows
   .\dev.bat quality
   ```

2. **Stage your changes:**
   ```bash
   git add .
   ```

3. **Pre-commit hooks run automatically:**
   - Black formats code
   - isort sorts imports
   - Ruff lints code
   - Bandit checks security

4. **If hooks find issues:**
   - They auto-fix what they can
   - Re-stage and commit:
   ```bash
   git add .
   git commit -m "message"
   ```

## Manual Commands (All Platforms)

If you prefer running tools directly without make/batch scripts:

```bash
# Install dependencies
pip install black isort ruff mypy pytest bandit pre-commit

# Format code
black .
isort .

# Lint code
ruff check . --fix

# Type check
mypy .

# Run tests
pytest -v

# Install pre-commit hooks
pre-commit install

# Run pre-commit manually
pre-commit run --all-files
```

## IDE Integration

### VS Code
1. Install "Black Formatter" extension (ms-python.black-formatter)
2. Install "isort" extension (ms-python.isort)
3. Format on save: Add to `.vscode/settings.json`:
   ```json
   "[python]": {
     "editor.formatOnSave": true,
     "editor.defaultFormatter": "ms-python.black-formatter",
     "editor.codeActionsOnSave": {
       "source.organizeImports": true
     }
   }
   ```

### PyCharm
- Black: Settings → Tools → Python Integrated Tools → Black
- isort: Settings → Tools → Python Integrated Tools → isort
- Enable "Reformat code" and "Rearrange imports" on save

## Troubleshooting

**Commands not found:**
- Linux/macOS: Make sure `make` is installed: `brew install make` (macOS)
- Windows: Use `.\dev.bat` instead of `dev.bat`

**Pre-commit hook issues:**
- Reinstall: `pre-commit install`
- Skip on commit (not recommended): `git commit --no-verify`

**Import errors in Mypy:**
- May require type stubs: `pip install types-<package>`
- Some issues are expected; focus on your own code

**Black vs Editor formatting conflict:**
- Configure editor to use Black formatter (see IDE Integration)
- Line length should be 100 (already configured)
