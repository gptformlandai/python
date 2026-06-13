# Hands-On: Copy-Paste Working Example

## Setup in 5 Minutes

### Step 1: Create Project Directory
```bash
mkdir my-firstpkg
cd my-firstpkg
```

### Step 2: Create Folder Structure
```bash
mkdir -p src/mypkg tests
touch README.md LICENSE
```

### Step 3: Create `src/mypkg/__init__.py`
```python
"""My awesome first package!"""

__version__ = "1.0.0"
__author__ = "Your Name"

from .utils import greet, add

__all__ = ["greet", "add", "__version__"]
```

### Step 4: Create `src/mypkg/utils.py`
```python
"""Utility functions."""

def greet(name: str) -> str:
    """Greet someone.
    
    Args:
        name: Person's name
        
    Returns:
        Greeting message
        
    Examples:
        >>> greet("Alice")
        'Hello, Alice!'
    """
    return f"Hello, {name}!"


def add(a: float, b: float) -> float:
    """Add two numbers.
    
    Args:
        a: First number
        b: Second number
        
    Returns:
        Sum of a and b
        
    Examples:
        >>> add(2, 3)
        5
    """
    return a + b
```

### Step 5: Create `tests/test_utils.py`
```python
"""Tests for utils module."""

import pytest
from mypkg.utils import greet, add


class TestGreet:
    """Test greet function."""
    
    def test_greet_simple(self):
        """Test simple greeting."""
        assert greet("Alice") == "Hello, Alice!"
    
    def test_greet_empty(self):
        """Test greeting with empty string."""
        assert greet("") == "Hello, !"


class TestAdd:
    """Test add function."""
    
    def test_add_positive(self):
        """Test adding positive numbers."""
        assert add(2, 3) == 5
    
    def test_add_negative(self):
        """Test adding negative numbers."""
        assert add(-2, -3) == -5
    
    def test_add_mixed(self):
        """Test adding mixed numbers."""
        assert add(2, -3) == -1
```

### Step 6: Create `pyproject.toml` (THE KEY FILE!)
```toml
[build-system]
requires = ["setuptools>=69", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "my-firstpkg"
version = "1.0.0"
description = "My first Python package!"
readme = "README.md"
requires-python = ">=3.8"
authors = [
    {name = "Your Name", email = "your.email@example.com"}
]
keywords = ["tutorial", "example"]
classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
]

[project.optional-dependencies]
dev = ["pytest>=7.0"]

[project.urls]
Homepage = "https://github.com/yourname/my-firstpkg"
Repository = "https://github.com/yourname/my-firstpkg.git"
Issues = "https://github.com/yourname/my-firstpkg/issues"

[tool.setuptools]
package-dir = {"" = "src"}
packages = ["mypkg"]
```

### Step 7: Create `README.md`
```markdown
# My First Package

A simple example Python package.

## Installation

```bash
pip install my-firstpkg
```

## Usage

```python
from mypkg import greet, add

print(greet("World"))  # Hello, World!
print(add(5, 3))       # 8
```

## Development

```bash
# Install in dev mode
pip install -e ".[dev]"

# Run tests
pytest tests/
```
```

### Step 8: Create `LICENSE`
```
MIT License

Copyright (c) 2024 Your Name

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

---

## Your Project Structure Now

```
my-firstpkg/
├── src/
│   └── mypkg/
│       ├── __init__.py
│       └── utils.py
├── tests/
│   └── test_utils.py
├── pyproject.toml          ← THE MAGIC!
├── README.md
└── LICENSE
```

---

## Run These Commands (Copy-Paste!)

### Step 1: Install Tools
```bash
pip install build pytest twine
```

### Step 2: Install Your Package (Dev Mode)
```bash
pip install -e .
```

### Step 3: Test Import
```bash
python -c "from mypkg import greet, add; print(greet('World')); print(add(5, 3))"
```

Expected output:
```
Hello, World!
8
```

### Step 4: Run Tests
```bash
pytest tests/ -v
```

Expected output:
```
tests/test_utils.py::TestGreet::test_greet_simple PASSED
tests/test_utils.py::TestGreet::test_greet_empty PASSED
tests/test_utils.py::TestAdd::test_add_positive PASSED
tests/test_utils.py::TestAdd::test_add_negative PASSED
tests/test_utils.py::TestAdd::test_add_mixed PASSED

======================== 5 passed in 0.05s ========================
```

### Step 5: Build Distributions
```bash
python -m build
```

Expected output:
```
* Creating virtualenv isolated build environment...
* Installing packages in isolated environment...
  ✓ Successful
* Getting build backend...
* Building sdist...
* Building wheel...
* Successfully built my_firstpkg-1.0.0.tar.gz and my_firstpkg-1.0.0-py3-none-any.whl
```

### Step 6: Check What Was Created
```bash
ls -lh dist/
```

Expected output:
```
-rw-r--r--  4.2K my_firstpkg-1.0.0-py3-none-any.whl
-rw-r--r--  3.1K my_firstpkg-1.0.0.tar.gz
```

### Step 7: Inspect the Wheel
```bash
unzip -l dist/my_firstpkg-1.0.0-py3-none-any.whl
```

Expected output:
```
Archive:  dist/my_firstpkg-1.0.0-py3-none-any.whl
  Length      Date    Time    Name
---------  ---------- -----   ----
      150  01-01-1980 00:00   mypkg/__init__.py
      280  01-01-1980 00:00   mypkg/utils.py
      110  01-01-1980 00:00   my_firstpkg-1.0.0.dist-info/WHEEL
      450  01-01-1980 00:00   my_firstpkg-1.0.0.dist-info/METADATA
      280  01-01-1980 00:00   my_firstpkg-1.0.0.dist-info/RECORD
```

### Step 8: Validate Before Publishing (if publishing to PyPI)
```bash
twine check dist/*
```

Expected output:
```
Checking distribution dist/my_firstpkg-1.0.0-py3-none-any.whl: PASSED
Checking distribution dist/my_firstpkg-1.0.0.tar.gz: PASSED
```

---

## What Happened Behind the Scenes?

### When you ran `pip install -e .`:

```
1. pip read pyproject.toml
2. pip found [build-system] section
3. pip verified setuptools>=69 installed ✓
4. pip verified wheel installed ✓
5. pip called: setuptools.build_meta.build_wheel()
6. setuptools found src/mypkg/
7. setuptools identified __init__.py exists
8. setuptools created my_firstpkg-1.0.0-py3-none-any.whl
9. pip extracted wheel to site-packages/
10. pip created symlink to src/mypkg/
   (because of -e flag, changes to .py files are immediately visible)
11. Done! Now `import mypkg` works
```

### When you ran `python -m build`:

```
1. build tool read pyproject.toml
2. build tool created isolated virtualenv
3. build tool installed setuptools + wheel into isolated env
4. build tool called: build_wheel()
5. setuptools created .whl (binary)
6. build tool called: build_sdist()
7. setuptools created .tar.gz (source)
8. build tool created dist/ folder
9. build tool wrote both files
10. build tool destroyed isolated env (cleanup)
11. Done! Both distributions ready
```

---

## Interactive Session: Step-by-Step

### Terminal 1: Setup
```bash
# Create and enter directory
mkdir my-firstpkg && cd my-firstpkg

# Create structure
mkdir -p src/mypkg tests

# Copy files from above into place
# (src/mypkg/__init__.py, src/mypkg/utils.py, etc.)

# Install build tools
pip install build pytest twine
```

### Terminal 2: Develop
```bash
# Install package in dev mode
pip install -e .

# Now you can import anywhere
python
>>> from mypkg import greet, add
>>> greet("Python")
'Hello, Python!'
>>> add(10, 20)
30
>>> exit()
```

### Terminal 3: Test
```bash
# Run tests
pytest tests/ -v

# All tests pass!
```

### Terminal 4: Build
```bash
# Build distributions
python -m build

# Check output
ls -lh dist/

# Inspect wheel
unzip -l dist/*.whl

# Validate
twine check dist/*
```

---

## Common First-Time Mistakes & Fixes

### Mistake 1: "ModuleNotFoundError: No module named 'mypkg'"

**Cause:** Forgot `pip install -e .`

**Fix:**
```bash
pip install -e .
```

---

### Mistake 2: "No module named 'setuptools'"

**Cause:** Missing setuptools

**Fix:**
```bash
pip install setuptools>=69 wheel
```

---

### Mistake 3: Wheel file is empty/corrupted

**Cause:** Didn't run `python -m build` correctly

**Fix:**
```bash
# Clean everything
rm -rf dist/ build/ *.egg-info src/*.egg-info

# Rebuild
python -m build
```

---

### Mistake 4: "pyproject.toml not found"

**Cause:** Running from wrong directory or missing file

**Fix:**
```bash
# Make sure you're in project root
ls pyproject.toml

# If not present, create it (copy from Step 6 above)
```

---

### Mistake 5: Version mismatch

**Cause:** Changed version in pyproject.toml but didn't rebuild

**Fix:**
```bash
# Clean and rebuild
rm -rf dist/ build/ *.egg-info
python -m build
```

---

## Uninstall Your Package

```bash
# If installed in dev mode
pip uninstall my-firstpkg

# Or force-uninstall
pip uninstall -y my-firstpkg

# Verify
pip show my-firstpkg  # Should say: WARNING: Package(s) not found
```

---

## Next Steps

1. ✅ **Done!** You've built your first package
2. 📦 **Consider:** Add more modules to `src/mypkg/`
3. 📝 **Consider:** Expand tests in `tests/`
4. 🌐 **Consider:** Publish to PyPI (see QUICK_REFERENCE.md)
5. 📚 **Consider:** Add documentation with Sphinx
6. 🔄 **Consider:** Add CI/CD with GitHub Actions

---

## Pro Tips for Next Time

### Tip 1: Use Templates
```bash
pip install cookiecutter
cookiecutter https://github.com/audreyr/cookiecutter-pypackage
```

### Tip 2: Keep Version in One Place
```python
# src/mypkg/__init__.py
__version__ = "1.0.0"
```

Then in pyproject.toml:
```toml
version = "1.0.0"
```

Or use dynamic versioning (advanced).

### Tip 3: Start with src/ Layout
```
✅ GOOD:
my-pkg/
├── src/
│   └── mypkg/

❌ BAD:
my-pkg/
├── mypkg/
```

Reason: Avoids accidentally importing from source instead of installed version.

### Tip 4: Always Include Tests
```bash
pytest tests/
```

### Tip 5: Use Pre-commit Hooks
```bash
pip install pre-commit
# Create .pre-commit-config.yaml
pre-commit install
```

---

**Congratulations!** You now know Python packaging! 🎉
