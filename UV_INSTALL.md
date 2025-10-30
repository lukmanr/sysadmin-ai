# Installing SysAdmin AI with uv

## What is uv?

[uv](https://github.com/astral-sh/uv) is an extremely fast Python package installer and resolver, written in Rust by Astral (the creators of Ruff). It's designed as a drop-in replacement for pip and pip-tools.

### Why use uv?

- ⚡ **10-100x faster** than pip for dependency resolution and installation
- 🦀 **Written in Rust** for maximum performance
- 🔒 **Drop-in replacement** for pip with the same interface
- 📦 **Better dependency resolution** algorithm
- 🎯 **Modern tooling** with great UX

## Quick Start

### 1. Install with the automated script (Recommended)

```bash
./install-uv.sh
```

This script will:
1. Install uv automatically if not present
2. Install all Python dependencies using uv
3. Set up the `ai` alias
4. Configure your environment

### 2. Manual installation

#### Step 1: Install uv

**macOS and Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows:**
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**With pip (any platform):**
```bash
pip install uv
```

**With Homebrew (macOS):**
```bash
brew install uv
```

#### Step 2: Install dependencies

```bash
# System-wide installation
uv pip install --system -r requirements.txt

# Or user installation
uv pip install -r requirements.txt

# Or in a virtual environment
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -r requirements.txt
```

#### Step 3: Set up the alias

```bash
./setup-alias.sh
```

### 3. Install as a Python package

You can also install sysadmin-ai as a proper Python package:

```bash
# Install directly
uv pip install .

# Or in a virtual environment
uv venv
source .venv/bin/activate
uv pip install .
```

After this, the `ai` and `sysadmin-ai` commands will be available system-wide (or in your venv).

## Comparison: uv vs pip

### Speed Test Example

Installing the dependencies for this project:

```bash
# With pip (traditional)
time pip install -r requirements.txt
# Real: ~15-30 seconds (first time)

# With uv
time uv pip install -r requirements.txt
# Real: ~1-3 seconds (first time)
```

**Result: uv is typically 10-20x faster!**

### Feature Comparison

| Feature | pip | uv |
|---------|-----|-----|
| Speed | Baseline | 10-100x faster |
| Dependency resolution | Good | Excellent |
| Disk cache | Yes | Yes (more efficient) |
| Virtual environments | venv | Built-in `uv venv` |
| Lock files | pip-tools | Built-in |
| Written in | Python | Rust |

## Using uv for Development

### Create a virtual environment

```bash
# Create venv
uv venv

# Activate it
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows

# Install dependencies
uv pip install -r requirements.txt
```

### Install in editable mode

```bash
uv pip install -e .
```

Now you can edit the code and changes will be reflected immediately.

### Sync dependencies

```bash
# Install/update all dependencies
uv pip sync requirements.txt
```

## Troubleshooting

### uv not found after installation

If you just installed uv, you may need to:

```bash
# Source the cargo environment
source $HOME/.cargo/env

# Or add to your shell config (~/.bashrc, ~/.zshrc, etc.)
export PATH="$HOME/.cargo/bin:$PATH"

# Or restart your terminal
```

### Permission errors

If you get permission errors:

```bash
# Use user installation instead of system
uv pip install -r requirements.txt

# Or use a virtual environment
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

### Falling back to pip

If uv doesn't work for any reason, you can always fall back to the traditional pip installation:

```bash
./install.sh
```

## Additional Resources

- [uv Documentation](https://github.com/astral-sh/uv)
- [uv Installation Guide](https://github.com/astral-sh/uv#installation)
- [Astral Blog](https://astral.sh/blog)

## Performance Tips

1. **Use `uv venv`** instead of `python -m venv` for faster virtual environment creation
2. **Cache is automatic** - uv caches packages globally for faster reinstalls
3. **Parallel downloads** - uv downloads and installs packages in parallel
4. **Better resolution** - uv's dependency resolver is more efficient than pip's

## Migration from pip

uv is designed as a drop-in replacement for pip. Most pip commands work with uv:

```bash
# pip commands
pip install package
pip install -r requirements.txt
pip list
pip show package
pip uninstall package

# uv equivalents (just replace 'pip' with 'uv pip')
uv pip install package
uv pip install -r requirements.txt
uv pip list
uv pip show package
uv pip uninstall package
```

Happy fast installing! 🚀

