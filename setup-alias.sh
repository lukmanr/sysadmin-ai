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

# SysAdmin AI Alias Setup Script

# Don't exit on error - we want to handle failures gracefully
# set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCRIPT_PATH="$SCRIPT_DIR/sysadmin_ai.py"

echo "🔧 Setting up SysAdmin AI alias..."
echo ""

# Check if the script exists
if [ ! -f "$SCRIPT_PATH" ]; then
    echo "❌ Error: sysadmin_ai.py not found in $SCRIPT_DIR"
    exit 1
fi

# Make sure the script is executable (non-fatal if it fails)
chmod +x "$SCRIPT_PATH" 2>/dev/null || echo "⚠️  Note: Could not set executable permission (may already be set or no write permission)"

# Detect OS for proper command generation
OS_INFO=$("$SCRIPT_PATH" --show-os 2>/dev/null | head -2 | tail -1 | cut -d: -f2 | xargs)

echo "✅ Detected system: $OS_INFO"
echo ""

# Determine shell configuration file
SHELL_CONFIG=""
if [ -n "$ZSH_VERSION" ]; then
    SHELL_CONFIG="$HOME/.zshrc"
    SHELL_NAME="zsh"
elif [ -n "$BASH_VERSION" ]; then
    if [ "$(uname)" = "Darwin" ]; then
        # macOS uses .bash_profile for login shells
        SHELL_CONFIG="$HOME/.bash_profile"
    else
        SHELL_CONFIG="$HOME/.bashrc"
    fi
    SHELL_NAME="bash"
else
    # Default to bashrc
    SHELL_CONFIG="$HOME/.bashrc"
    SHELL_NAME="bash"
fi

echo "📝 Shell configuration file: $SHELL_CONFIG"

# Create alias command
ALIAS_CMD="alias ai='$SCRIPT_PATH'"

# Check if alias already exists
if [ -f "$SHELL_CONFIG" ] && grep -q "alias ai=" "$SHELL_CONFIG"; then
    echo "⚠️  Alias 'ai' already exists in $SHELL_CONFIG"
    echo "Current alias:"
    grep "alias ai=" "$SHELL_CONFIG"
    echo ""
    read -p "Replace existing alias? [y/N]: " replace
    if [[ "$replace" =~ ^[Yy]$ ]]; then
        # Remove existing alias
        sed -i.bak '/alias ai=/d' "$SHELL_CONFIG"
        echo "🗑️  Removed existing alias"
    else
        echo "❌ Alias setup cancelled"
        exit 0
    fi
fi

# Add the alias
echo "" >> "$SHELL_CONFIG"
echo "# SysAdmin AI alias" >> "$SHELL_CONFIG"
echo "$ALIAS_CMD" >> "$SHELL_CONFIG"

echo "✅ Added alias to $SHELL_CONFIG"
echo ""

# Create ~/.local/bin if it doesn't exist and try to create symlink
if [ ! -d "$HOME/.local/bin" ]; then
    echo "📁 Creating ~/.local/bin directory..."
    if mkdir -p "$HOME/.local/bin" 2>/dev/null; then
        echo "✅ Created ~/.local/bin directory"
    else
        echo "⚠️  Warning: Could not create ~/.local/bin directory"
        echo "ℹ️  Skipping symlink creation"
        USER_BIN_AVAILABLE=false
    fi
else
    USER_BIN_AVAILABLE=true
fi

if [ "$USER_BIN_AVAILABLE" != "false" ] && [ -d "$HOME/.local/bin" ]; then
    SYMLINK_PATH="$HOME/.local/bin/ai"
    if [ -L "$SYMLINK_PATH" ] || [ -f "$SYMLINK_PATH" ]; then
        echo "⚠️  File/symlink already exists at $SYMLINK_PATH"
        read -p "Replace it? [y/N]: " replace_symlink
        if [[ "$replace_symlink" =~ ^[Yy]$ ]]; then
            rm -f "$SYMLINK_PATH"
            if ln -sf "$SCRIPT_PATH" "$SYMLINK_PATH" 2>/dev/null; then
                echo "✅ Created symlink: $SYMLINK_PATH"
            else
                echo "⚠️  Warning: Failed to create symlink at $SYMLINK_PATH"
                echo "   You can create it manually with:"
                echo "   ln -sf '$SCRIPT_PATH' '$SYMLINK_PATH'"
            fi
        fi
    else
        if ln -sf "$SCRIPT_PATH" "$SYMLINK_PATH" 2>/dev/null; then
            echo "✅ Created symlink: $SYMLINK_PATH"
        else
            echo "⚠️  Warning: Failed to create symlink at $SYMLINK_PATH"
            echo "   You can create it manually with:"
            echo "   ln -sf '$SCRIPT_PATH' '$SYMLINK_PATH'"
        fi
    fi
    
    # Check if ~/.local/bin is in PATH
    if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
        echo ""
        echo "⚠️  Note: $HOME/.local/bin is not in your PATH"
        echo "Add this to your $SHELL_CONFIG:"
        echo 'export PATH="$HOME/.local/bin:$PATH"'
    fi
else
    echo "ℹ️  Symlink creation skipped - ~/.local/bin not available"
fi

echo ""
echo "🎉 Alias setup complete!"
echo ""
echo "📋 To start using the 'ai' command:"
echo "1. Reload your shell configuration:"
echo "   source $SHELL_CONFIG"
echo ""
echo "2. Or start a new terminal session"
echo ""
echo "3. Test the alias:"
echo "   ai --help"
echo "   ai \"show disk usage\""
echo ""
echo "💡 The tool has been configured for: $OS_INFO"
echo "   Commands will be optimized for your system!"
echo ""

# Show a sample of what the user can do
echo "🚀 Quick start examples:"
echo "   ai \"check system memory\""
echo "   ai \"show running processes\""
echo "   ai \"find large files in /tmp\""
echo "   ai --interactive"
