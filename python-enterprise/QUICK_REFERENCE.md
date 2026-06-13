# Quick Reference & Cheat Sheet

## 1-Minute Summary

```
[build-system]
requires = ["setuptools>=69", "wheel"]
build-backend = "setuptools.build_meta"

↓ Means:

When someone runs: pip install mypackage

1. pip reads this section
2. pip ensures setuptools>=69 is installed
3. pip ensures wheel is installed
4. pip calls setuptools to build your package
5. setuptools creates two files:
   - .tar.gz (source)
   - .whl (binary)
6. pip installs the .whl
7. Done!
```

---

## Visual Comparison: Build Systems

```
SETUPTOOLS (Most Common)
├─ Pros:  Mature, flexible, standard
├─ Cons:  Complex, legacy baggage
├─ Best:  Complex projects, C extensions
└─ Files: pyproject.toml + optional setup.py

POETRY (Popular, Modern)
├─ Pros:  Simple, includes dep management
├─ Cons:  Lock files, slower
├─ Best:  Full project management
└─ Files: pyproject.toml only

FLIT (Lightweight)
├─ Pros:  Very simple, fast
├─ Cons:  Limited features
├─ Best:  Simple packages
└─ Files: pyproject.toml only

HATCH (Next-Gen)
├─ Pros:  Modern, well-designed
├─ Cons:  Newer, less adoption
├─ Best:  Modern projects
└─ Files: pyproject.toml only

PDM (Cutting Edge)
├─ Pros:  Future-proof, PEP 621
├─ Cons:  Very new
├─ Best:  Forward-thinking teams
└─ Files: pyproject.toml only
```

---

## Decision Tree: Which Build System?

```
START: Choosing a build system
│
├─ Already using Poetry? ──→ USE POETRY
│
├─ Need C extensions? ──→ USE SETUPTOOLS
│
├─ Simple script? ──→ USE FLIT
│
├─ Modern project? ──→ USE HATCH or PDM
│
└─ Default/Unsure? ──→ USE SETUPTOOLS
   (Most compatible, most docs, biggest community)
```

---

## Command Cheat Sheet

### Installation & Building
```bash
# Install build tools
pip install build twine

# Build distributions (.tar.gz + .whl)
python -m build

# Build only wheel
python -m build --wheel

# Build only source dist
python -m build --sdist

# Install locally (development mode)
pip install -e .

# Install with optional dependencies
pip install -e ".[dev]"
```

### Publishing
```bash
# Check distributions before publishing
twine check dist/*

# Upload to PyPI
twine upload dist/*

# Upload to TestPyPI (test first)
twine upload --repository testpypi dist/*
```

### Inspection
```bash
# List wheel contents
unzip -l dist/*.whl

# Extract wheel for inspection
unzip dist/*.whl -d /tmp/wheel

# Show package info
pip show mycalculator

# Show dependencies
pip list
pipdeptree -p mycalculator
```

### Development
```bash
# Run tests
pytest tests/

# Format code
black src/

# Check style
flake8 src/

# Type check
mypy src/

# Build documentation
sphinx-build -b html docs/ build/
```

---

## File Template: pyproject.toml

```toml
[build-system]
requires = ["setuptools>=69", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "mypackage"
version = "1.0.0"
description = "Short description"
readme = "README.md"
requires-python = ">=3.8"
authors = [
    {name = "Your Name", email = "you@example.com"}
]
license = {text = "MIT"}
keywords = ["keyword1", "keyword2"]

[project.urls]
Homepage = "https://github.com/user/mypackage"
Documentation = "https://mypackage.readthedocs.io"
Repository = "https://github.com/user/mypackage.git"

[project.optional-dependencies]
dev = ["pytest", "black", "mypy"]
docs = ["sphinx", "sphinx-rtd-theme"]

[tool.setuptools.packages]
find = {where = ["src"]}

[tool.black]
line-length = 88
```

---

## File Sizes & Download Times

```
Typical Python Package:

Size        Download Time (1 Mbps)    Build Time
────────────────────────────────────────────────
Source (.tar.gz)
  Simple    100 KB                 1s          3-5s
  Medium    500 KB                 4s          5-10s
  Large     5 MB                   40s         30-60s

Wheel (.whl)
  Simple    80 KB                  1s          0s (instant!)
  Medium    400 KB                 3s          0s
  Large     4 MB                   32s         0s

Popular Packages:
  pandas        200 MB              1600s       (pre-built wheels available)
  numpy         100 MB              800s        (pre-built wheels available)
  django        5 MB                40s         10s
  requests      300 KB              2s          1s
```

---

## Platform Tags Explained

### When .whl filename matters

```
numpy-1.21.0-cp39-cp39-win_amd64.whl
├─ Works on: Windows 64-bit
├─ Requires: Python 3.9 CPython
├─ Contains: Compiled C code
└─ Download: Specific to your system

numpy-1.21.0-py3-none-any.whl
├─ Works on: Any platform!
├─ Requires: Any Python 3.x
├─ Contains: Pure Python
└─ Download: Universal

flask-2.0.0-py3-none-any.whl
├─ Works on: Any platform
├─ Requires: Any Python 3.x
├─ Contains: Pure Python
└─ Download: Use this (fastest!)
```

### Tag Components

```
File: package-version-python-abi-platform.whl

Python Tags:
  py2, py3     Generic
  py27, py38   Specific versions
  cp39         CPython 3.9
  pp37         PyPy 3.7

ABI Tags:
  none         Pure Python
  cp39         CPython 3.9 ABI
  abi3         Stable ABI

Platform Tags:
  any          Any platform (best!)
  win_amd64    Windows 64-bit
  manylinux1   Linux (many versions)
  macosx_10_9  macOS 10.9+
```

---

## Project Structure Templates

### Minimal (Simple Package)
```
mypackage/
├── src/
│   └── mypackage/
│       ├── __init__.py
│       └── module.py
├── pyproject.toml
└── README.md
```

### Standard (Medium Project)
```
mypackage/
├── src/
│   └── mypackage/
│       ├── __init__.py
│       ├── module1.py
│       └── module2.py
├── tests/
│   ├── __init__.py
│   ├── test_module1.py
│   └── test_module2.py
├── docs/
│   ├── conf.py
│   ├── index.rst
│   └── api.rst
├── pyproject.toml
├── README.md
├── LICENSE
└── CHANGELOG.md
```

### Enterprise (Complex Project)
```
mycompany-package/
├── src/
│   └── mycompany_pkg/
│       ├── __init__.py
│       ├── core/
│       │   ├── __init__.py
│       │   └── engine.py
│       ├── utils/
│       │   ├── __init__.py
│       │   └── helpers.py
│       └── cli/
│           ├── __init__.py
│           └── commands.py
├── tests/
│   ├── unit/
│   ├── integration/
│   └── fixtures/
├── docs/
│   ├── source/
│   └── build/
├── scripts/
│   ├── release.sh
│   └── benchmark.py
├── .github/workflows/
│   └── ci.yml
├── pyproject.toml
├── setup.cfg
├── tox.ini
├── .pre-commit-config.yaml
├── README.md
├── CONTRIBUTING.md
├── LICENSE
├── CHANGELOG.md
└── .gitignore
```

---

## Understanding .whl Filename

### Anatomy

```
mycalculator-1.0.0-py3-none-any.whl
└───┬────────┬───┬──┬────┬─┬──┬───
    │        │   │  │    │ │  └─ Platform (any)
    │        │   │  │    │ └─ ABI (none/pure Python)
    │        │   │  │    └─ Implementation (py3)
    │        │   │  └──── Release tag
    │        │   └─ Build tag (optional)
    │        └─ Version
    └─ Package name (lowercase, underscore-to-hyphen)
```

### Examples Decoded

```
Flask-2.0.0-py3-none-any.whl
  │     │    │  │    │  │
  │     │    │  │    │  └─ Any OS (Unix, Windows, macOS)
  │     │    │  │    └─ Pure Python (no native code)
  │     │    │  └─ Works with any Python 3.x
  │     │    └─ No build number
  │     └─ Version 2.0.0
  └─ Package Flask

numpy-1.23.0-cp310-cp310-win_amd64.whl
  │    │      │     │     │  │
  │    │      │     │     │  └─ Windows 64-bit only
  │    │      │     │     └─ CPython 3.10 ABI (compiled code)
  │    │      │     └─ CPython 3.10 required
  │    │      └─ No build number
  │    └─ Version 1.23.0
  └─ Package numpy
```

---

## Debugging Checklist

### Package won't install
```
❌ After running: pip install mypackage

Check:
□ Is pyproject.toml in root?
□ Is [build-system] defined?
□ Does setuptools>=69 exist? (pip install setuptools)
□ Does wheel exist? (pip install wheel)
□ Is package name correct? (lowercase, hyphens)
□ Do you have permission to write to site-packages?
```

### Package installs but import fails
```
❌ After: pip install -e .
   Then: python -c "import mypackage"

Check:
□ Is src/mypackage/ or mypackage/ present?
□ Does __init__.py exist in package?
□ Is Python path correct? (python -c "import sys; print(sys.path)")
□ Did you forget to run pip install? (should be installed to site-packages)
```

### Wheel file broken
```
❌ After: python -m build
   Then: unzip dist/*.whl fails

Check:
□ Run: twine check dist/*
□ Check disk space (build needs space)
□ Check file permissions
□ Try: rm -rf build/ dist/ && python -m build --wheel
```

### Version mismatch
```
❌ Version in code ≠ Version in package

Check:
□ Is version in pyproject.toml correct?
□ Is __init__.py version synced?
□ Did you update version before rebuilding?
□ Clear old builds: rm -rf dist/ build/
```

---

## Common Mistakes & Fixes

| Mistake | Problem | Solution |
|---------|---------|----------|
| No `pyproject.toml` | pip doesn't know how to build | Create it with `[build-system]` |
| Wrong package dir | Import fails | Use `src/` layout with `[tool.setuptools.package-dir]` |
| Missing `__init__.py` | Package not recognized | Add `__init__.py` to each package dir |
| Forgetting to install | Code not accessible | Run `pip install -e .` |
| Not updating version | Users get wrong version | Update in `pyproject.toml` before `build` |
| Including test files | Package too large | Use `[tool.setuptools.packages]` to exclude |
| Old setup.py only | PEP 517 won't work | Create modern `pyproject.toml` |
| Too many deps | Package installs slow | Reduce dependencies, use optional deps |

---

## Performance Tips

### Make installation faster

```
DO:
✅ Use wheels for distribution
✅ Keep dependencies minimal
✅ Use optional dependencies for extras
✅ Cache packages locally
✅ Pre-build wheels for all platforms

DON'T:
❌ Distribute only source (.tar.gz)
❌ Add unnecessary dependencies
❌ Require compilation on install
❌ Make deps too strict (e.g., ==1.2.3)
```

### Make builds faster

```
DO:
✅ Use caching (pip cache)
✅ Pre-compute expensive operations
✅ Use binary packages where possible
✅ Parallel builds (if supported)

DON'T:
❌ Download dependencies during build
❌ Compile code unnecessarily
❌ Fetch from network during build
```

---

## Security Considerations

### When building packages

```
SECURE:
✅ Use pyproject.toml (declarative, no code execution)
✅ Pin dependency versions
✅ Sign distributions with GPG
✅ Use checksums (RECORD file)
✅ Publish to official PyPI only

INSECURE:
❌ setup.py with arbitrary Python code
❌ Running pip from untrusted sources
❌ Not verifying packages
❌ Using unsigned distributions
❌ Old setuptools (update regularly)
```

### When installing packages

```
SECURE:
✅ pip install package (from PyPI)
✅ Verify checksums
✅ Use virtual environments
✅ Keep pip updated

INSECURE:
❌ pip install from random URL
❌ setup.py develop (arbitrary code)
❌ Installing as root
❌ Old Python versions
```

---

## Version Numbering (Semantic Versioning)

```
Version: MAJOR.MINOR.PATCH

1.0.0
│ │ │
│ │ └─ Patch: Bug fixes (1.0.1)
│ └─── Minor: New features (1.1.0)
└───── Major: Breaking changes (2.0.0)

Examples:
0.1.0  → Initial development release
1.0.0  → First stable release
1.0.1  → Bug fix
1.1.0  → New feature (backward compatible)
2.0.0  → Breaking change (new major version)
2.0.1  → Bug fix on version 2
2.1.0  → New feature on version 2
```

---

## Resources

### Official Documentation
- PEP 517 (Build System Interface): https://www.python.org/dev/peps/pep-0517/
- PEP 518 (pyproject.toml): https://www.python.org/dev/peps/pep-0518/
- setuptools docs: https://setuptools.pypa.io/
- Wheel format: https://packaging.python.org/specifications/binary-distribution-format/
- PyPI: https://pypi.org/

### Tools
- build: Build packages (`python -m build`)
- twine: Upload packages (`twine upload`)
- flit: Simple build backend
- poetry: Full package manager
- hatch: Modern project manager

### Online Resources
- Python Packaging User Guide: https://packaging.python.org/
- Real Python (packaging article)
- Full Stack Python (Packaging)

---

## Final Checklist: Before Publishing

```
□ Bump version in pyproject.toml
□ Update CHANGELOG.md
□ Run tests: pytest tests/
□ Run linter: flake8
□ Run formatter: black --check
□ Build: python -m build
□ Check: twine check dist/*
□ Install locally: pip install dist/*.whl
□ Test import: python -c "import mypackage"
□ Clean: rm -rf build/ dist/ *.egg-info/
□ Build again: python -m build
□ Upload to TestPyPI first
□ Verify on TestPyPI
□ Upload to PyPI: twine upload dist/*
□ Verify on PyPI
□ Push git tag: git tag v1.0.0 && git push --tags
□ Announce release!
```

---

You're now ready to package Python like a pro! 🚀
