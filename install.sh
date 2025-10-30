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

# SysAdmin AI Installation Script

# Removed 'set -e' to allow graceful handling of non-critical failures

echo "🤖 Installing SysAdmin AI..."
echo ""

# Check for Python 3
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is required but not found"
    echo "Please install Python 3.7 or higher"
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Function to suggest pip installation based on OS
suggest_pip_installation() {
    echo ""
    echo "📦 pip3 is not installed. Here's how to install it:"
    echo ""
    
    # Detect OS and provide appropriate commands
    if [ "$(uname)" = "Darwin" ]; then
        # macOS
        echo "For macOS:"
        echo "  # Using Homebrew (recommended):"
        echo "  brew install python"
        echo ""
        echo "  # Or using the official Python installer:"
        echo "  # Download from https://python.org and pip will be included"
        echo ""
        echo "  # Or if you have Python but missing pip:"
        echo "  curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py"
        echo "  python3 get-pip.py"
        
    elif [ -f /etc/os-release ]; then
        # Linux - detect distribution
        . /etc/os-release
        case $ID in
            ubuntu|debian)
                echo "For Ubuntu/Debian:"
                echo "  sudo apt update"
                echo "  sudo apt install python3-pip"
                ;;
            fedora)
                echo "For Fedora:"
                echo "  sudo dnf install python3-pip"
                ;;
            centos|rhel)
                echo "For CentOS/RHEL:"
                echo "  sudo yum install epel-release"
                echo "  sudo yum install python3-pip"
                echo ""
                echo "  # Or for newer versions:"
                echo "  sudo dnf install python3-pip"
                ;;
            arch|manjaro)
                echo "For Arch Linux:"
                echo "  sudo pacman -S python-pip"
                ;;
            opensuse*|sles)
                echo "For openSUSE:"
                echo "  sudo zypper install python3-pip"
                ;;
            alpine)
                echo "For Alpine Linux:"
                echo "  sudo apk add py3-pip"
                ;;
            *)
                echo "For your Linux distribution ($PRETTY_NAME):"
                echo "  # Try one of these common approaches:"
                echo "  sudo apt install python3-pip     # Debian/Ubuntu"
                echo "  sudo yum install python3-pip     # CentOS/RHEL"
                echo "  sudo dnf install python3-pip     # Fedora"
                echo "  sudo pacman -S python-pip        # Arch"
                ;;
        esac
    else
        # Generic Unix/Linux
        echo "For your system:"
        echo "  # Try the universal pip installer:"
        echo "  curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py"
        echo "  python3 get-pip.py"
        echo ""
        echo "  # Or check your package manager:"
        echo "  # Most systems: python3-pip or python-pip package"
    fi
    
    echo ""
    echo "After installing pip, run this script again:"
    echo "  ./install.sh"
}

# Check for pip
if ! command -v pip3 &> /dev/null && ! python3 -m pip --version &> /dev/null; then
    echo "❌ pip3 is required but not found"
    suggest_pip_installation
    exit 1
fi

echo "✅ pip found"

# Install dependencies
echo ""
echo "📦 Installing Python dependencies..."

# Try to install dependencies with better error handling
install_deps() {
    if command -v pip3 &> /dev/null; then
        pip3 install -r requirements.txt --user
    else
        python3 -m pip install -r requirements.txt --user
    fi
}

if ! install_deps; then
    echo ""
    echo "❌ Failed to install Python dependencies"
    echo ""
    echo "💡 Troubleshooting tips:"
    echo "  1. Try installing without --user flag (system-wide):"
    if command -v pip3 &> /dev/null; then
        echo "     sudo pip3 install -r requirements.txt"
    else
        echo "     sudo python3 -m pip install -r requirements.txt"
    fi
    echo ""
    echo "  2. Try upgrading pip first:"
    echo "     python3 -m pip install --upgrade pip"
    echo ""
    echo "  3. On some systems, you may need to install python3-dev:"
    echo "     sudo apt install python3-dev python3-setuptools  # Ubuntu/Debian"
    echo "     sudo yum install python3-devel                   # CentOS/RHEL"
    echo ""
    echo "  4. If you're using a virtual environment:"
    echo "     python3 -m venv venv"
    echo "     source venv/bin/activate"
    echo "     pip install -r requirements.txt"
    echo ""
    exit 1
fi

echo "✅ Dependencies installed"

# Make scripts executable (non-fatal if they fail)
echo ""
echo "🔧 Setting up executables..."
chmod +x sysadmin_ai.py 2>/dev/null || echo "⚠️  Note: Could not set executable permission on sysadmin_ai.py (may already be set or no write permission)"
chmod +x package-sysadmin-ai.py 2>/dev/null || echo "⚠️  Note: Could not set executable permission on package-sysadmin-ai.py (may already be set or no write permission)"
chmod +x demo.sh 2>/dev/null || echo "⚠️  Note: Could not set executable permission on demo.sh (may already be set or no write permission)"
chmod +x setup-alias.sh 2>/dev/null || echo "⚠️  Note: Could not set executable permission on setup-alias.sh (may already be set or no write permission)"

echo "✅ Executable permissions configured"

# Detect OS and show information (non-fatal if it fails)
echo ""
echo "🔍 Detecting system..."
if OS_DETECTED=$(./sysadmin_ai.py --show-os 2>/dev/null | grep "Detected OS:" | cut -d: -f2 | xargs); then
    echo "✅ Detected: $OS_DETECTED"
else
    echo "⚠️  Note: Could not detect OS automatically (this is normal if dependencies aren't installed yet)"
    echo "   The tool will auto-detect when you run it with your API key"
fi

# Set up alias (non-fatal if it fails)
echo ""
echo "🔧 Setting up 'ai' alias..."
if ! ./setup-alias.sh; then
    echo "⚠️  Warning: Alias setup encountered issues, but installation can continue"
    echo "   You can run './setup-alias.sh' manually later to set up the alias"
fi

# Create additional symlink in user's local bin if it exists (for backward compatibility)
if [ -d "$HOME/.local/bin" ]; then
    if ln -sf "$(pwd)/sysadmin_ai.py" "$HOME/.local/bin/sysadmin-ai" 2>/dev/null; then
        echo "✅ Created symlink: $HOME/.local/bin/sysadmin-ai"
    else
        echo "⚠️  Note: Could not create symlink in $HOME/.local/bin (no write permission)"
        echo "   You can create it manually with:"
        echo "   ln -sf '$(pwd)/sysadmin_ai.py' '$HOME/.local/bin/sysadmin-ai'"
    fi
    
    # Check if ~/.local/bin is in PATH
    if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
        echo ""
        echo "⚠️  Note: $HOME/.local/bin is not in your PATH"
        echo "Add this to your ~/.bashrc or ~/.zshrc:"
        echo 'export PATH="$HOME/.local/bin:$PATH"'
    fi
else
    echo "ℹ️  $HOME/.local/bin doesn't exist, skipping additional symlink creation"
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
echo "   ./sysadmin_ai.py --interactive"
echo ""
echo "5. Try the demo:"
echo "   ./demo.sh"
echo ""
echo "Happy system administration! 🚀"
