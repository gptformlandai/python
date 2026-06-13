# Advanced: Deep Dive into Build Process

## What Happens When You Run `pip install .`

### Second-by-second breakdown:

```
$ pip install .

STEP 1: Discover Configuration (0.1s)
┌─────────────────────────────────────────┐
│ pip searches for:                       │
│ ✓ pyproject.toml (FOUND)               │
│                                         │
│ pip reads [build-system]:              │
│ ✓ requires = ["setuptools>=69", "wheel"]│
│ ✓ backend = "setuptools.build_meta"    │
└─────────────────────────────────────────┘

STEP 2: Check Build Dependencies (0.5s)
┌─────────────────────────────────────────┐
│ Current environment has:                │
│ setuptools 69.0.0? ✓ YES               │
│ wheel 0.40.0? ✓ YES                    │
│                                         │
│ (If not installed: pip downloads them) │
└─────────────────────────────────────────┘

STEP 3: Invoke Build Backend (1-3s)
┌─────────────────────────────────────────┐
│ pip imports:                            │
│ from setuptools.build_meta import *    │
│                                         │
│ Calls:                                  │
│ build_wheel(wheel_directory, ...)      │
└─────────────────────────────────────────┘

STEP 4a: Analyze Source Code
┌─────────────────────────────────────────┐
│ setuptools scans:                       │
│ ├─ Find all .py files                  │
│ ├─ Parse imports                       │
│ ├─ Identify package structure          │
│ └─ Check for C extensions              │
└─────────────────────────────────────────┘

STEP 4b: Generate Metadata
┌─────────────────────────────────────────┐
│ Creates dist-info directory:            │
│ ├─ METADATA (from pyproject.toml)      │
│ ├─ WHEEL (format info)                  │
│ ├─ RECORD (file inventory)              │
│ ├─ entry_points.txt (CLI tools)         │
│ └─ top_level.txt (package names)        │
└─────────────────────────────────────────┘

STEP 4c: Create Wheel
┌─────────────────────────────────────────┐
│ 1. Create .whl file (ZIP archive)      │
│ 2. Add package code                    │
│ 3. Add dist-info/ directory            │
│ 4. Calculate checksums (RECORD)        │
│ 5. Save to: dist/ folder               │
└─────────────────────────────────────────┘

STEP 5: Extract and Install
┌─────────────────────────────────────────┐
│ 1. Unzip .whl to site-packages/        │
│ 2. Write installed files list          │
│ 3. Register with pip                   │
│ 4. Install dependencies (if any)       │
└─────────────────────────────────────────┘

STEP 6: Verify Installation
┌─────────────────────────────────────────┐
│ $ pip show mycalculator                │
│ Name: mycalculator                     │
│ Version: 1.0.0                         │
│ Location: /path/to/site-packages       │
│ Requires: (none if no deps)            │
└─────────────────────────────────────────┘
```

---

## The Wheel File: Detailed Anatomy

A `.whl` file is just a ZIP archive! Let's explore:

### File Structure Inside
```
mycalculator-1.0.0-py3-none-any.whl
├── mycalculator/                    # Your package
│   ├── __init__.py
│   ├── calculator.py
│   └── py.typed
│
└── mycalculator-1.0.0.dist-info/    # Metadata folder
    ├── WHEEL                        # Format spec
    ├── METADATA                     # Package info
    ├── RECORD                       # File inventory
    ├── entry_points.txt             # CLI commands
    ├── top_level.txt                # Top-level modules
    └── licenses/                    # License files
        └── LICENSE
```

### Detailed: WHEEL File
```
Wheel-Version: 1.0
Generator: bdist_wheel (0.37.1)
Root-Is-Purelib: true
Tag: py3-none-any
```

**Explained:**
- `Root-Is-Purelib: true` = Pure Python (no C extensions)
- `Tag: py3-none-any` = Works on any Python 3, any OS, any architecture

### Detailed: METADATA File
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
Classifier: License :: OSI Approved :: MIT License
Classifier: Programming Language :: Python :: 3
Classifier: Programming Language :: Python :: 3.8
Description-Content-Type: text/x-rst
Requires-Python: >=3.8
```

This is what pip reads to:
- ✅ Check if package is compatible
- ✅ Find dependencies
- ✅ Display info in `pip show`

### Detailed: RECORD File
```
mycalculator/__init__.py,sha256=abc123...,150
mycalculator/calculator.py,sha256=def456...,280
mycalculator-1.0.0.dist-info/WHEEL,sha256=ghi789...,110
mycalculator-1.0.0.dist-info/METADATA,sha256=jkl012...,450
mycalculator-1.0.0.dist-info/RECORD,,
```

**Format:** `filename,hash,size`

Used for:
- ✅ Verification (checksums)
- ✅ Uninstall (knows what to delete)
- ✅ Integrity checking

---

## The .tar.gz: Source Distribution

### Structure
```
mycalculator-1.0.0.tar.gz (compressed)
└── mycalculator-1.0.0/ (uncompressed)
    ├── src/
    │   └── mycalculator/
    │       ├── __init__.py
    │       └── calculator.py
    ├── tests/
    │   └── test_calculator.py
    ├── pyproject.toml
    ├── README.md
    ├── LICENSE
    └── PKG-INFO          # Metadata (copy of METADATA)
```

### When Installed from .tar.gz

```
1. Download mycalculator-1.0.0.tar.gz (~10 KB)
2. Extract it
3. Read pyproject.toml
4. Install build deps (setuptools, wheel)
5. Call build backend
6. Generate .whl
7. Install from .whl
8. Clean up temp files
```

**This is slower** because of steps 3-6!

---

## Wheel Filename Convention

### Pattern: `{distribution}-{version}(-{build tag})?-{python}-{abi}-{platform}.whl`

#### Example: `mycalculator-1.0.0-py3-none-any.whl`

```
mycalculator     = Distribution name (package name)
1.0.0            = Version
py3              = Python tag (py3 = any Python 3.x)
none             = ABI tag (none = pure Python)
any              = Platform tag (any = all platforms)
```

#### More examples:

```
Package          Python Ver   ABI              Platform
─────────────────────────────────────────────────────────
numpy-py27       py27         cp27m            win_amd64
numpy-py38       py38         cp38             manylinux

Flask-py3        py3          none             any
pillow-py37      py37         cp37m            win32
```

### Tag Meanings

| Tag | Meaning |
|-----|---------|
| `py3` | Python 3.x (any 3.x version) |
| `cp39` | CPython 3.9 (specific) |
| `pp37` | PyPy 3.7 |
| `cp27mu` | CPython 2.7 (unicode) |
| `none` | Pure Python (no compiled code) |
| `cp39` (ABI) | CPython 3.9 ABI (compiled code) |
| `any` | Any platform |
| `win_amd64` | Windows 64-bit |
| `manylinux1_x86_64` | Linux (many versions) |

---

## PEP 517: The Foundation

### What is PEP 517?

A Python Enhancement Proposal that standardized:
1. **How to build packages** (build backends)
2. **What tools are needed** (declared in pyproject.toml)
3. **Separation of concerns** (build deps separate from runtime)

### Before PEP 517 (❌ Problems)

```python
# setup.py was the standard
# Problems:
# 1. Arbitrary Python code could run
# 2. Had to install build tools first
# 3. No isolation between build and runtime deps
# 4. Hard for tools to understand

import numpy  # PROBLEM: Forces numpy install!
from setuptools import setup

setup(
    name="mypackage",
    ext_modules=[Extension("my_ext", sources=["src/my_ext.c"])]
)
```

### After PEP 517 (✅ Clean)

```toml
# pyproject.toml is declarative
# Benefits:
# 1. No arbitrary code execution
# 2. Dependencies explicitly listed
# 3. Build tools isolated
# 4. Tools can parse without executing

[build-system]
requires = ["setuptools>=69", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "mypackage"
# No random imports!
```

---

## Build Backend Hooks

### What setuptools.build_meta provides

```python
# These are the functions pip calls:

build_wheel(wheel_directory, config_settings=None, metadata_directory=None)
    # Creates .whl file
    # Returns: "mycalculator-1.0.0-py3-none-any.whl"

build_sdist(sdist_directory, config_settings=None)
    # Creates .tar.gz file
    # Returns: "mycalculator-1.0.0.tar.gz"

get_requires_for_build_wheel(config_settings=None)
    # Returns: ["setuptools>=69", "wheel"]

get_requires_for_build_sdist(config_settings=None)
    # Returns: ["setuptools>=69", "wheel"]

prepare_metadata_for_build_wheel(metadata_directory, config_settings=None)
    # Returns: directory containing METADATA file
```

---

## Environment Variables & Configuration

### What Happens Behind the Scenes

```bash
# When you run:
pip install .

# pip internally does (simplified):
export PIP_BUILD_DIR=/tmp/pip-build-xyz
export PYTHONPATH=/tmp/pip-build-xyz:$PYTHONPATH

# Create isolated environment
python -m venv /tmp/build-env
source /tmp/build-env/bin/activate

# Install build deps
pip install "setuptools>=69" "wheel"

# Import and call backend
python -c "
from setuptools.build_meta import build_wheel
build_wheel('/path/to/dist')
"

# Extract wheel
unzip -d /usr/local/lib/python3.9/site-packages dist/*.whl

# Cleanup
rm -rf /tmp/build-env /tmp/pip-build-xyz
```

---

## Debugging the Build Process

### See what's happening

```bash
# Verbose output
pip install -e . -v

# Very verbose
pip install -e . -vv

# Debug mode (lots of output)
pip install -e . -vvv

# Keep build directory for inspection
pip install --no-clean -e .
# Build files stay in /tmp/pip-build-xyz
```

### Check wheel contents

```bash
# List files
unzip -l dist/mycalculator-1.0.0-py3-none-any.whl

# Extract for inspection
unzip dist/mycalculator-1.0.0-py3-none-any.whl -d /tmp/wheel-contents

# View METADATA
cat /tmp/wheel-contents/mycalculator-1.0.0.dist-info/METADATA

# View WHEEL file
cat /tmp/wheel-contents/mycalculator-1.0.0.dist-info/WHEEL

# View RECORD
cat /tmp/wheel-contents/mycalculator-1.0.0.dist-info/RECORD
```

### Verify wheel

```bash
# Check integrity
unzip -t dist/mycalculator-1.0.0-py3-none-any.whl

# Validate with twine
twine check dist/*

# Check dependencies
pip install pipdeptree
pipdeptree -p mycalculator
```

---

## Performance: .whl vs .tar.gz

### Installation Time Comparison

```
Package Size: 1 MB

From .tar.gz:
├─ Download: 0.5 MB (5s @ 100 KB/s)
├─ Extract: (2s)
├─ Read metadata: (1s)
├─ Analyze/Build: (8s)  ← EXTRA!
├─ Install: (2s)
└─ Total: ~18s

From .whl:
├─ Download: 0.8 MB (8s @ 100 KB/s)
├─ Extract: (1s)
├─ Install: (2s)
└─ Total: ~11s         ← 40% faster!
```

### Why Distribute Both?

1. **Wheels** for most users (fast)
2. **Source dist** for:
   - Users on uncommon platforms
   - People building from source
   - Version pinning/reproducibility
   - Security audits (see source code)

---

## Common Installation Methods

### Method 1: From PyPI
```bash
pip install mycalculator
# pip finds .whl, downloads, installs (fastest!)
```

### Method 2: Development Install
```bash
cd my-calculator
pip install -e .
# Installs with symlink to source
# Changes to source code immediately visible!
```

### Method 3: From Local File
```bash
pip install dist/mycalculator-1.0.0-py3-none-any.whl
# Install pre-built wheel
```

### Method 4: From Git
```bash
pip install git+https://github.com/user/my-calculator.git
# pip clones repo, builds, installs
```

### Method 5: From Directory
```bash
pip install .
# Builds wheel first, then installs
```

---

## Summary: The Complete Pipeline

```
┌──────────────────────────────────────────────────────────────┐
│                    YOU WRITE                                 │
│  (mypackage/, tests/, pyproject.toml)                       │
└──────────────┬───────────────────────────────────────────────┘
               │
               ▼
    ┌──────────────────────┐
    │  Run: pip install .  │
    └──────────┬───────────┘
               │
        ┌──────┴─────────┐
        │                │
        ▼                ▼
    ┌─────────────┐  ┌──────────────┐
    │ .tar.gz     │  │ .whl         │
    │ (source)    │  │ (binary)     │
    └──────┬──────┘  └────────┬─────┘
           │                  │
           │      ┌───────────┴─────────────┐
           │      │                         │
           ▼      ▼                         ▼
     ┌──────────────────────────────────────────┐
     │  PyPI Repository                        │
     │  (Central package registry)             │
     └──────────────┬───────────────────────────┘
                    │
         ┌──────────┴──────────┐
         │                     │
         ▼                     ▼
    ┌─────────────┐    ┌──────────────┐
    │ Other users │    │ Your project │
    │ pip install │    │ colleagues   │
    └─────────────┘    └──────────────┘
```

This is enterprise-grade Python packaging! 🚀
