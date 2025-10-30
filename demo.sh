#!/bin/bash
# SysAdmin AI Demo Script

echo "==================================="
echo "🤖 SysAdmin AI Demo"
echo "==================================="
echo ""

echo "This demo shows the SysAdmin AI tool in action."
echo "Note: This requires a valid ANTHROPIC_API_KEY to be set."
echo ""

# Check if API key is available
if [ -z "$ANTHROPIC_API_KEY" ] && [ ! -f ".env.secrets" ]; then
    echo "⚠️  Warning: No API key found."
    echo "Set ANTHROPIC_API_KEY environment variable or create .env.secrets file"
    echo ""
    echo "Example:"
    echo "export ANTHROPIC_API_KEY='your_key_here'"
    echo "# or"
    echo "echo 'ANTHROPIC_API_KEY=your_key_here' > .env.secrets"
    echo ""
    echo "For demo purposes, we'll show the tool interface without API calls..."
    echo ""
fi

echo "1. Showing help:"
echo "=================="
./sysadmin-ai.py --help
echo ""

echo "2. Showing version:"
echo "==================="
./sysadmin-ai.py --version
echo ""

echo "3. Example commands and questions you could run:"
echo "================================================"
cat << 'EOF'
# Interactive mode:
./sysadmin-ai.py --interactive

# Single commands:
./sysadmin-ai.py "show disk usage"
./sysadmin-ai.py "find large files in /tmp"
./sysadmin-ai.py "check system memory"

# Questions (NEW Q&A feature):
./sysadmin-ai.py "what is uvx and where does it install files?"
./sysadmin-ai.py "how do I configure SSH key authentication?"
./sysadmin-ai.py "what's the difference between systemctl and service?"

# With safety options:
./sysadmin-ai.py --safe-mode "clean temporary files"
./sysadmin-ai.py --auto-confirm "list running processes"

# All processed with intelligent intent detection - no special syntax needed!

# Configuration:
./sysadmin-ai.py --config

# Create embedded version:
./sysadmin-ai.py --embed-key sysadmin-ai-embedded.py
EOF

echo ""
echo "4. Package creation examples:"
echo "============================="
cat << 'EOF'
# Create portable package:
./package-sysadmin-ai.py --portable sysadmin-ai-portable

# Create standalone version:
./package-sysadmin-ai.py --standalone sysadmin-ai-standalone.py

# Create all versions:
./package-sysadmin-ai.py --all
EOF

echo ""
echo "5. Quick test (safe mode, no API call):"
echo "======================================="
echo "Testing basic functionality..."

# Test configuration creation
echo "Creating test configuration..."
python3 -c "
import sys
sys.path.insert(0, '.')
from pathlib import Path
import json

# Create a test config
config = {
    'model': 'claude-4-5-haiku-latest',
    'max_tokens': 1000,
    'auto_confirm': False,
    'log_commands': True,
    'safe_mode': True,
    'command_timeout': 300
}

config_file = Path.home() / '.sysadmin-ai.json'
with open(config_file, 'w') as f:
    json.dump(config, f, indent=2)

print(f'✅ Test configuration created at {config_file}')
"

echo ""
echo "==================================="
echo "✅ Demo complete!"
echo ""
echo "Next steps:"
echo "1. Set your ANTHROPIC_API_KEY"
echo "2. Run: ./sysadmin-ai.py --interactive"
echo "3. Try commands like 'show disk usage'"
echo "4. Try questions like 'what is docker?'"
echo "5. Claude automatically determines your intent"
echo "6. Web search is enabled by default for current info"
echo "==================================="
