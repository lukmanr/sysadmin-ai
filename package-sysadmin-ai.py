#!/usr/bin/env python3
# Copyright (c) 2025 Lukman Ramsey
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""
Packaging script for SysAdmin AI
Creates self-contained executable versions
"""

import os
import sys
import shutil
import subprocess
import tempfile
import argparse
from pathlib import Path

def check_dependencies():
    """Check if required tools are available"""
    required_tools = ['python3', 'pip']
    
    for tool in required_tools:
        if not shutil.which(tool):
            print(f"Error: {tool} not found in PATH")
            return False
    
    return True

def install_dependencies(temp_dir: Path):
    """Install dependencies in temporary directory"""
    print("Installing dependencies...")
    
    # Create requirements.txt in temp directory
    requirements = """requests>=2.31.0
cryptography>=41.0.0"""
    
    with open(temp_dir / 'requirements.txt', 'w') as f:
        f.write(requirements)
    
    # Install dependencies
    cmd = [
        sys.executable, '-m', 'pip', 'install',
        '-r', str(temp_dir / 'requirements.txt'),
        '--target', str(temp_dir / 'libs')
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Failed to install dependencies: {result.stderr}")
        return False
    
    return True

def create_standalone_script(output_file: str, embed_key: bool = False):
    """Create standalone script with bundled dependencies"""
    
    if not check_dependencies():
        return False
    
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Install dependencies
        if not install_dependencies(temp_path):
            return False
        
        # Read original script
        with open('sysadmin_ai.py', 'r') as f:
            original_content = f.read()
        
        # Create standalone version
        standalone_content = f'''#!/usr/bin/env python3
"""
SysAdmin AI - Standalone Version
Auto-generated standalone executable with bundled dependencies
"""

import sys
import os
from pathlib import Path

# Add bundled libraries to path
SCRIPT_DIR = Path(__file__).parent
LIB_DIR = SCRIPT_DIR / "libs"
if LIB_DIR.exists():
    sys.path.insert(0, str(LIB_DIR))

# If running as a bundled script, adjust imports
try:
    # Original script content follows
{original_content}
except ImportError as e:
    print(f"Missing dependency: {{e}}")
    print("This standalone version requires Python 3.7+")
    print("If you continue to have issues, install dependencies manually:")
    print("pip install requests cryptography")
    sys.exit(1)
'''
        
        # Write standalone script
        with open(output_file, 'w') as f:
            f.write(standalone_content)
        
        # Make executable
        os.chmod(output_file, 0o755)
        
        # Copy libraries if they exist
        lib_source = temp_path / 'libs'
        lib_dest = Path(output_file).parent / 'libs'
        
        if lib_source.exists():
            if lib_dest.exists():
                shutil.rmtree(lib_dest)
            shutil.copytree(lib_source, lib_dest)
        
        print(f"Created standalone script: {output_file}")
        if lib_dest.exists():
            print(f"Dependencies bundled in: {lib_dest}")
        
        return True

def create_portable_package(output_dir: str):
    """Create a portable package directory"""
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    # Copy main script
    shutil.copy('sysadmin_ai.py', output_path / 'sysadmin_ai.py')
    
    # Copy requirements
    shutil.copy('requirements.txt', output_path / 'requirements.txt')
    
    # Create install script
    install_script = '''#!/bin/bash
# SysAdmin AI Installation Script

set -e

echo "Installing SysAdmin AI..."

# Check for Python 3
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required but not found"
    exit 1
fi

# Install dependencies
echo "Installing Python dependencies..."
python3 -m pip install -r requirements.txt --user

# Make script executable
chmod +x sysadmin_ai.py

# Create symlink in user's local bin if it exists
if [ -d "$HOME/.local/bin" ]; then
    ln -sf "$(pwd)/sysadmin_ai.py" "$HOME/.local/bin/sysadmin-ai"
    echo "Created symlink: $HOME/.local/bin/sysadmin-ai"
fi

echo "Installation complete!"
echo ""
echo "Usage:"
echo "  ./sysadmin_ai.py --help"
echo "  ./sysadmin_ai.py --interactive"
echo ""
echo "If ~/.local/bin is in your PATH, you can also run:"
echo "  sysadmin-ai --help"
'''
    
    with open(output_path / 'install.sh', 'w') as f:
        f.write(install_script)
    
    os.chmod(output_path / 'install.sh', 0o755)
    
    # Create README
    readme = '''# SysAdmin AI - Portable Package

This is a portable package of SysAdmin AI, a natural language command-line tool for Unix/Linux system administration.

## Installation

Run the install script:

```bash
./install.sh
```

This will:
1. Install required Python dependencies
2. Make the script executable
3. Create a symlink in ~/.local/bin (if it exists)

## Manual Installation

If you prefer to install manually:

```bash
# Install dependencies
pip install -r requirements.txt

# Make executable
chmod +x sysadmin_ai.py
```

## Usage

Interactive mode:
```bash
./sysadmin_ai.py --interactive
```

Single command:
```bash
./sysadmin_ai.py "show disk usage"
```

Get help:
```bash
./sysadmin_ai.py --help
```

## API Key Setup

The tool looks for your Anthropic API key in the following order:
1. ANTHROPIC_API_KEY environment variable
2. .env.secrets file in the current directory
3. Prompt for manual entry

Create a .env.secrets file:
```
ANTHROPIC_API_KEY=your_api_key_here
```

## Features

- Natural language to bash command translation
- Interactive and single-command modes
- Safety checks for dangerous commands
- Command history and logging
- Configurable settings
- Embedded API key support

## Security

- Safe mode prevents execution of dangerous commands
- User confirmation before command execution
- Command validation and warnings
- Optional command logging

Enjoy using SysAdmin AI!
'''
    
    with open(output_path / 'README.md', 'w') as f:
        f.write(readme)
    
    print(f"Created portable package in: {output_path}")
    print("Run './install.sh' in that directory to install")
    
    return True

def main():
    parser = argparse.ArgumentParser(description='Package SysAdmin AI for distribution')
    parser.add_argument('--standalone', metavar='OUTPUT_FILE', 
                       help='Create standalone script with bundled dependencies')
    parser.add_argument('--portable', metavar='OUTPUT_DIR', 
                       help='Create portable package directory')
    parser.add_argument('--all', action='store_true', 
                       help='Create both standalone and portable versions')
    
    args = parser.parse_args()
    
    if args.all:
        print("Creating all package types...")
        create_standalone_script('sysadmin-ai-standalone.py')
        create_portable_package('sysadmin-ai-portable')
        
    elif args.standalone:
        create_standalone_script(args.standalone)
        
    elif args.portable:
        create_portable_package(args.portable)
        
    else:
        parser.print_help()
        print("\nExample usage:")
        print("  python3 package-sysadmin-ai.py --standalone sysadmin-ai-standalone.py")
        print("  python3 package-sysadmin-ai.py --portable sysadmin-ai-portable")
        print("  python3 package-sysadmin-ai.py --all")

if __name__ == "__main__":
    main()
