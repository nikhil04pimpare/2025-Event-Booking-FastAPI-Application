@echo off
REM Development utilities for Windows
REM Usage: dev.bat <command>

setlocal enabledelayedexpansion

if "%1%"=="" (
    call :show_help
    exit /b 0
)

set "command=%1"

if /i "%command%"=="help" goto show_help
if /i "%command%"=="install" goto install
if /i "%command%"=="format" goto format
if /i "%command%"=="lint" goto lint
if /i "%command%"=="typecheck" goto typecheck
if /i "%command%"=="quality" goto quality
if /i "%command%"=="test" goto test
if /i "%command%"=="clean" goto clean
if /i "%command%"=="precommitinstall" goto precommitinstall
if /i "%command%"=="precommitrun" goto precommitrun
if /i "%command%"=="dev" goto dev

call :show_help
exit /b 0

:show_help
echo Available commands:
echo   dev install            - Install project dependencies
echo   dev format             - Format code with Black and isort
echo   dev lint               - Run Ruff linter
echo   dev typecheck          - Run Mypy type checker
echo   dev quality            - Run all quality checks
echo   dev test               - Run tests with pytest
echo   dev clean              - Remove cache and build files
echo   dev precommitinstall   - Install pre-commit hooks
echo   dev precommitrun       - Run pre-commit on all files
echo   dev dev                - Setup complete development environment
echo   dev help               - Show this help message
goto end

:install
echo Installing dependencies...
pip install -e .
pip install black isort ruff mypy pytest bandit pre-commit
echo ✅ Dependencies installed!
goto end

:format
echo Formatting code...
python -m black .
python -m isort .
echo ✅ Code formatted!
goto end

:lint
echo Running Ruff linter...
python -m ruff check . --fix
echo ✅ Linting complete!
goto end

:typecheck
echo Running Mypy type checker...
python -m mypy .
echo ✅ Type checking complete!
goto end

:quality
echo Running all quality checks...
call :format
call :lint
call :typecheck
echo ✅ All quality checks passed!
goto end

:test
echo Running tests...
python -m pytest -v
goto end

:clean
echo Cleaning cache and build files...
for /d /r . %%d in (__pycache__) do @if exist "%%d" (rmdir /s /q "%%d" >nul 2>&1)
for /d /r . %%d in (.pytest_cache) do @if exist "%%d" (rmdir /s /q "%%d" >nul 2>&1)
for /d /r . %%d in (.mypy_cache) do @if exist "%%d" (rmdir /s /q "%%d" >nul 2>&1)
for /d /r . %%d in (.ruff_cache) do @if exist "%%d" (rmdir /s /q "%%d" >nul 2>&1)
for /r . %%f in (*.pyc) do @if exist "%%f" (del /q "%%f" >nul 2>&1)
for /r . %%f in (*.egg-info) do @if exist "%%f" (del /q "%%f" >nul 2>&1)
echo ✅ Cache cleaned!
goto end

:precommitinstall
echo Installing pre-commit hooks...
python -m pre_commit install
echo ✅ Pre-commit hooks installed!
goto end

:precommitrun
echo Running pre-commit on all files...
python -m pre_commit run --all-files
echo ✅ Pre-commit checks complete!
goto end

:dev
echo Setting up development environment...
call :install
call :precommitinstall
echo ✅ Development environment setup complete!
goto end

:end
endlocal
