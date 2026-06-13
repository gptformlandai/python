# Practical Example: Building Your First Package

## Part 1: Project Structure Setup

Here's a working example you can replicate:

```
my-calculator/
├── src/
│   └── mycalculator/
│       ├── __init__.py
│       └── calculator.py
├── tests/
│   └── test_calculator.py
├── pyproject.toml
├── README.md
└── LICENSE
```

## Part 2: Create the Files

### 1. `src/mycalculator/__init__.py`
```python
"""A simple calculator package."""

__version__ = "1.0.0"

from .calculator import add, multiply, subtract, divide

__all__ = ["add", "multiply", "subtract", "divide"]
```

### 2. `src/mycalculator/calculator.py`
```python
"""Calculator functions."""

def add(a: float, b: float) -> float:
    """Add two numbers."""
    return a + b

def subtract(a: float, b: float) -> float:
    """Subtract two numbers."""
    return a - b

def multiply(a: float, b: float) -> float:
    """Multiply two numbers."""
    return a * b

def divide(a: float, b: float) -> float:
    """Divide two numbers."""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
```

### 3. `pyproject.toml` (THE MOST IMPORTANT FILE)
```toml
[build-system]
requires = ["setuptools>=69", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "mycalculator"
version = "1.0.0"
description = "A simple calculator package"
readme = "README.md"
requires-python = ">=3.8"
authors = [
    {name = "Your Name", email = "your.email@example.com"}
]
license = {text = "MIT"}
keywords = ["calculator", "math"]
classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "Topic :: Software Development :: Libraries",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
]

[project.optional-dependencies]
dev = ["pytest>=7.0", "black", "flake8"]

[project.urls]
Homepage = "https://github.com/yourname/mycalculator"
Documentation = "https://mycalculator.readthedocs.io"
Repository = "https://github.com/yourname/mycalculator.git"
Issues = "https://github.com/yourname/mycalculator/issues"

[tool.setuptools]
packages = ["mycalculator"]

[tool.setuptools.package-dir]
"" = "src"
```

### 4. `README.md`
```markdown
# MyCalculator

A simple calculator package.

## Installation

```bash
pip install mycalculator
```

## Usage

```python
from mycalculator import add, multiply

result = add(5, 3)  # 8
product = multiply(4, 7)  # 28
```
```

### 5. `tests/test_calculator.py`
```python
"""Tests for calculator module."""

import pytest
from mycalculator import add, subtract, multiply, divide

def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0

def test_subtract():
    assert subtract(5, 3) == 2
    assert subtract(0, 5) == -5

def test_multiply():
    assert multiply(3, 4) == 12
    assert multiply(-2, 3) == -6

def test_divide():
    assert divide(10, 2) == 5.0
    
def test_divide_by_zero():
    with pytest.raises(ValueError):
        divide(5, 0)
```

## Part 3: Build Your Package

### Step 1: Install Build Tools
```bash
cd my-calculator
pip install build twine
```

### Step 2: Build Distributions
```bash
python -m build
```

### What Gets Created
```bash
dist/
├── mycalculator-1.0.0.tar.gz           # 5 KB (source)
└── mycalculator-1.0.0-py3-none-any.whl # 3 KB (wheel)
```

### Inspect the Wheel (it's just a ZIP!)
```bash
unzip -l dist/mycalculator-1.0.0-py3-none-any.whl
```

You'll see:
```
mycalculator/
├── __init__.py
├── calculator.py
└── py.typed

mycalculator-1.0.0.dist-info/
├── WHEEL
├── METADATA
├── RECORD
├── entry_points.txt
└── top_level.txt
```

## Part 4: Test Installation

### Install in Development Mode
```bash
# Install and link to source (for development)
pip install -e .
```

Now you can import it:
```python
from mycalculator import add
print(add(5, 3))  # Output: 8
```

### Or Install from Wheel
```bash
pip install dist/mycalculator-1.0.0-py3-none-any.whl
```

## Part 5: Understanding the Metadata

### What's in `METADATA`?
```
Metadata-Version: 2.1
Name: mycalculator
Version: 1.0.0
Summary: A simple calculator package
Home-page: https://github.com/yourname/mycalculator
Author: Your Name
Author-email: your.email@example.com
License: MIT
Platform: UNKNOWN
Classifier: Development Status :: 3 - Alpha
Classifier: Intended Audience :: Developers
Classifier: Topic :: Software Development :: Libraries
Classifier: License :: OSI Approved :: MIT License
Classifier: Programming Language :: Python :: 3
```

This is auto-generated from `pyproject.toml`!

### What's in `WHEEL`?
```
Wheel-Version: 1.0
Generator: bdist_wheel (0.37.1)
Root-Is-Purelib: true
Tag: py3-none-any
```

This tells pip:
- ✅ Pure Python (no compiled C extensions)
- ✅ Works on ANY OS
- ✅ Requires Python 3.x

## Part 6: Publish to PyPI

### Step 1: Create Account
Go to https://pypi.org and create account

### Step 2: Generate Token
In your PyPI account settings → API tokens

### Step 3: Upload
```bash
twine upload dist/*
```

Then users anywhere can:
```bash
pip install mycalculator
```

## Part 7: Version Bumping

When you fix bugs or add features:

### Update version in `pyproject.toml`:
```toml
version = "1.0.1"  # Patch fix
version = "1.1.0"  # New feature
version = "2.0.0"  # Breaking change
```

### Rebuild and re-upload:
```bash
rm dist/*
python -m build
twine upload dist/*
```

## Quick Commands Reference

```bash
# Setup
pip install build twine

# Development installation (linked to source)
pip install -e .

# Install dev dependencies
pip install -e ".[dev]"

# Build distributions
python -m build

# Test wheel before publishing
pip install dist/mycalculator-1.0.0-py3-none-any.whl

# Run tests
pytest tests/

# Format code
black src/ tests/

# Check style
flake8 src/ tests/

# Publish (check twice!)
twine check dist/*
twine upload dist/*
```

## Common Issues & Solutions

### Issue: "No module named setuptools"
```bash
pip install setuptools>=69
```

### Issue: Package not found after install
```bash
# Make sure you're in the right directory
pip install -e .

# Or explicitly specify the path
pip install /path/to/my-calculator
```

### Issue: Wheel file too large
- Strip unnecessary files
- Use `.wheelignore` or MANIFEST.in

### Issue: Version mismatch
- Keep `__init__.py` and `pyproject.toml` in sync
- Or use single source of truth (read version from file)

---

## What's Different From Old Setup.py?

### Old Way (❌ Don't use)
```python
# setup.py
from setuptools import setup

setup(
    name="mycalculator",
    version="1.0.0",
    description="A calculator",
    # ... 20 more lines
)
```

Issues:
- Python code is evaluated (security risk)
- Hard to parse for tools
- Mixing logic with configuration

### New Way (✅ Use this)
```toml
# pyproject.toml
[build-system]
requires = ["setuptools>=69", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "mycalculator"
version = "1.0.0"
description = "A calculator"
# ... clean, declarative
```

Benefits:
- Declarative (not imperative)
- Easy to parse for tools
- Secure (no code execution)
- Standard format (TOML)
