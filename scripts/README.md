# Scripts Directory

This directory contains utility scripts for the Aircon AI project.

## Scripts Overview

### `check_tools.py`

**Purpose**: Validates that all code formatting tools are installed and working correctly.

**Usage**:

```bash
python scripts/check_tools.py
```

**What it checks**:

- Black (code formatter)
- isort (import organizer)
  - pylint (style checker)
- autopep8 (PEP8 compliance)

### `format_code.py`

**Purpose**: Formats all Python code in the project according to PEP8 standards.

**Usage**:

```bash
python scripts/format_code.py
```

**What it does**:

- Organizes imports with isort
- Formats code with Black
  - Checks style compliance with pylint
- Reports formatting results

### `install_hooks.py`

**Purpose**: Installs git pre-commit hooks for automatic code formatting.

**Usage**:

```bash
python scripts/install_hooks.py
```

**What it installs**:

- Pre-commit hook that automatically formats staged Python files
- Hook runs before each git commit
- Ensures all committed code is properly formatted

### `pre_commit_hook.py`

**Purpose**: The actual pre-commit hook implementation (called automatically by git).

**Functionality**:

- Detects staged Python files
- Runs isort and Black on each file
- Re-stages formatted files
- Prevents commits if formatting fails

## Quick Start

1. **Check if tools are ready**:

   ```bash
   python scripts/check_tools.py
   ```

2. **Install dependencies** (if needed):

   ```bash
   pip install -r requirements.txt
   ```

3. **Format existing code**:

   ```bash
   python scripts/format_code.py
   ```

4. **Setup automatic formatting**:
   ```bash
   python scripts/install_hooks.py
   ```

## Integration with Make

All scripts can be run via Makefile commands:

```bash
make check        # Run check_tools.py
make format       # Run format_code.py
make setup-hooks  # Run install_hooks.py
make dev          # Full development setup
```
