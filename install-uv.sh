#!/bin/bash
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

# SysAdmin AI Installation Script using uv
# Fast, modern Python package installation with uv

set -e

echo "🤖 Installing SysAdmin AI with uv..."
echo ""

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "❌ uv is not installed"
    echo ""
    echo "📦 Installing uv..."
    echo ""
    
    # Detect OS and provide appropriate installation
    if [ "$(uname)" = "Darwin" ] || [ "$(uname)" = "Linux" ]; then
        # macOS or Linux - use the official installer
        echo "Running: curl -LsSf https://astral.sh/uv/install.sh | sh"
        curl -LsSf https://astral.sh/uv/install.sh | sh
        
        # Source the shell configuration to make uv available
        if [ -f "$HOME/.cargo/env" ]; then
            source "$HOME/.cargo/env"
        fi
        
        # Add to PATH for this session if not already there
        if [ -d "$HOME/.cargo/bin" ] && [[ ":$PATH:" != *":$HOME/.cargo/bin:"* ]]; then
            export PATH="$HOME/.cargo/bin:$PATH"
        fi
        
        echo ""
        echo "✅ uv installed successfully"
        echo ""
        echo "Note: You may need to restart your shell or run:"
        echo "  source \$HOME/.cargo/env"
        echo ""
    else
        echo "❌ Unsupported operating system for automatic uv installation"
        echo ""
        echo "Please install uv manually:"
        echo "  Visit: https://github.com/astral-sh/uv"
        echo ""
        exit 1
    fi
fi

# Verify uv is now available
if ! command -v uv &> /dev/null; then
    echo "❌ uv installation failed or not in PATH"
    echo ""
    echo "Please ensure uv is installed and in your PATH:"
    echo "  export PATH=\"\$HOME/.cargo/bin:\$PATH\""
    exit 1
fi

echo "✅ uv found: $(uv --version)"
echo ""

# Check for Python 3
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is required but not found"
    echo "Please install Python 3.7 or higher"
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"
echo ""

# Install dependencies using uv
echo "📦 Installing Python dependencies with uv..."
echo ""

# uv pip install is much faster than regular pip
if uv pip install --system -r requirements.txt; then
    echo ""
    echo "✅ Dependencies installed successfully"
else
    echo ""
    echo "❌ Failed to install dependencies with uv"
    echo ""
    echo "💡 Troubleshooting tips:"
    echo "  1. Try without --system flag (user install):"
    echo "     uv pip install -r requirements.txt"
    echo ""
    echo "  2. Try creating a virtual environment:"
    echo "     uv venv"
    echo "     source .venv/bin/activate  # or .venv/Scripts/activate on Windows"
    echo "     uv pip install -r requirements.txt"
    echo ""
    echo "  3. Fall back to regular pip:"
    echo "     ./install.sh"
    echo ""
    exit 1
fi

# Make scripts executable
echo ""
echo "🔧 Setting up executables..."
chmod +x sysadmin_ai.py 2>/dev/null || echo "⚠️  Note: Could not set executable permission on sysadmin_ai.py"
chmod +x package-sysadmin-ai.py 2>/dev/null || echo "⚠️  Note: Could not set executable permission on package-sysadmin-ai.py"
chmod +x demo.sh 2>/dev/null || echo "⚠️  Note: Could not set executable permission on demo.sh"
chmod +x setup-alias.sh 2>/dev/null || echo "⚠️  Note: Could not set executable permission on setup-alias.sh"

echo "✅ Executable permissions configured"

# Detect OS
echo ""
echo "🔍 Detecting system..."
if OS_DETECTED=$(./sysadmin_ai.py --show-os 2>/dev/null | grep "Detected OS:" | cut -d: -f2 | xargs); then
    echo "✅ Detected: $OS_DETECTED"
else
    echo "⚠️  Note: Could not detect OS automatically"
fi

# Set up alias
echo ""
echo "🔧 Setting up 'ai' alias..."
if ! ./setup-alias.sh; then
    echo "⚠️  Warning: Alias setup encountered issues"
    echo "   You can run './setup-alias.sh' manually later"
fi

# Create symlink in user's local bin if it exists
if [ -d "$HOME/.local/bin" ]; then
    if ln -sf "$(pwd)/sysadmin_ai.py" "$HOME/.local/bin/sysadmin-ai" 2>/dev/null; then
        echo "✅ Created symlink: $HOME/.local/bin/sysadmin-ai"
    else
        echo "⚠️  Note: Could not create symlink in $HOME/.local/bin"
    fi
    
    # Check if ~/.local/bin is in PATH
    if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
        echo ""
        echo "⚠️  Note: $HOME/.local/bin is not in your PATH"
        echo "Add this to your ~/.bashrc or ~/.zshrc:"
        echo 'export PATH="$HOME/.local/bin:$PATH"'
    fi
fi

echo ""
echo "🎉 Installation complete!"
echo ""
echo "📋 Next steps:"
echo "1. Set your Anthropic API key:"
echo "   export ANTHROPIC_API_KEY='your_api_key_here'"
echo ""
echo "2. Or create a .env.secrets file:"
echo "   echo 'ANTHROPIC_API_KEY=your_api_key_here' > .env.secrets"
echo ""
echo "3. Run the tool using the 'ai' alias:"
echo "   ai --help"
echo "   ai --interactive"
echo "   ai \"check system memory\""
echo ""
echo "4. Or run directly:"
echo "   ./sysadmin_ai.py --help"
echo ""
echo "5. Try the demo:"
echo "   ./demo.sh"
echo ""
echo "Happy system administration! 🚀"

