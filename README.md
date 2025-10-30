# SysAdmin AI 🤖⚡

[![PyPI version](https://badge.fury.io/py/sysadmin-ai.svg)](https://badge.fury.io/py/sysadmin-ai)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A powerful command-line tool that enables Unix/Linux system administration through natural language commands, powered by Claude AI.

## Features ✨

- **Natural Language Interface**: Describe what you want to do in plain English
- **Smart Command Translation**: Leverages Claude AI to convert natural language to appropriate bash commands
- **Question & Answer Mode**: Ask questions about Unix/Linux systems and get detailed explanations
- **Web Search Integration**: Automatically searches the web for up-to-date information when answering questions
- **Intelligent Mode Detection**: Automatically determines whether you're asking a question or requesting commands
- **Safety First**: Built-in dangerous command detection and safe mode
- **Multiple Deployment Options**: Standalone, portable, or embedded API key versions
- **Interactive & Script Modes**: Use interactively or in automation scripts
- **Command History & Logging**: Track and log all executed commands
- **Configurable Settings**: Customize behavior to match your workflow

## Quick Start 🚀

### Prerequisites

- Python 3.7 or higher
- Anthropic API key

### Installation

#### Option 1: Install from PyPI (Recommended - Easiest!)

The fastest way to get started is to install directly from PyPI:

```bash
# Using pip
pip install sysadmin-ai

# Or using uv (10-100x faster!)
uv pip install sysadmin-ai
```

After installation, the `ai` and `sysadmin-ai` commands will be available globally.

**Don't have uv?** Install it first for blazingly fast package management:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

#### Option 2: Install from Source with uv (Fast Development Setup)

[uv](https://github.com/astral-sh/uv) is a blazingly fast Python package installer and resolver written in Rust. It's 10-100x faster than pip!

1. **Clone the repository:**
   ```bash
   git clone https://github.com/lukmanr/sysadmin-ai.git
   cd sysadmin-ai/
   ```

2. **Run the uv installer:**
   ```bash
   ./install-uv.sh
   ```
   
   This will:
   - Install uv automatically if not present (macOS/Linux)
   - Check for Python 3
   - Install Python dependencies **much faster** than pip
   - Detect your operating system for optimal command generation
   - Set up the `ai` alias for easy access
   - Create symlinks and configure your shell

   **Why uv?**
   - ⚡ **10-100x faster** than pip for dependency resolution and installation
   - 🦀 Written in Rust for maximum performance
   - 🔒 Drop-in replacement for pip with the same interface
   - 📦 Better dependency resolution

   📖 **For detailed uv installation instructions and troubleshooting, see [UV_INSTALL.md](UV_INSTALL.md)**

#### Option 3: Install from Source with pip (Traditional)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/lukmanr/sysadmin-ai.git
   cd sysadmin-ai/
   ```

2. **Run the automated installer:**
   ```bash
   ./install.sh
   ```
   
   This will:
   - Check for Python 3 and pip (with helpful installation guidance if missing)
   - Install Python dependencies with error handling and troubleshooting tips
   - Detect your operating system for optimal command generation
   - Set up the `ai` alias for easy access
   - Create symlinks and configure your shell
   - Handle permission issues gracefully (script won't fail on chmod/symlink errors)

   **Multi-User Friendly**: The installer can be run by multiple users from the same directory. Each user gets their own alias and symlink configuration without affecting others.

   **Note**: If pip is missing, the installer will provide specific commands for your operating system to install it.

3. **Set up your API key:**
   ```bash
   export ANTHROPIC_API_KEY="your_api_key_here"
   ```
   
   Or create a `.env.secrets` file:
   ```
   ANTHROPIC_API_KEY=your_api_key_here
   ```

4. **Test the installation:**
   ```bash
   ai --help
   ai "show disk usage"
   ```

### Setting Up Your API Key

After installation (any method), configure your Anthropic API key:

```bash
# Option 1: Environment variable (recommended)
export ANTHROPIC_API_KEY="your_api_key_here"

# Option 2: Create a .env.secrets file in your working directory
echo 'ANTHROPIC_API_KEY=your_api_key_here' > ~/.sysadmin-ai-secrets

# Option 3: The tool will prompt you interactively if no key is found
```

### Quick Test

```bash
# Get help
ai --help

# Try a simple command
ai "show disk usage"

# Start interactive mode
ai --interactive
```

## Usage Examples 📝

### Easy Access with `ai` Command
After installation from PyPI or running the install scripts, you can use the short `ai` command:

```bash
# Interactive mode
ai --interactive

# Single commands
ai "show disk usage"
ai "check system memory"
ai "find large files in /tmp"
ai "list running services"
ai "show network connections"
```

### Interactive Mode
```bash
ai --interactive
```

Then type natural language commands:
```
sysadmin_ai> show me disk usage
sysadmin_ai> find large files in /var/log
sysadmin_ai> backup my home directory
sysadmin_ai> check which processes are using the most CPU
sysadmin_ai> update system packages
sysadmin_ai> restart apache service
sysadmin_ai> create a new user named john
sysadmin_ai> add user to sudo group
sysadmin_ai> check system memory usage
```

### Single Command Mode
```bash
# Commands
ai "show disk usage"
ai "find files larger than 100MB in /tmp" 
ai "check system memory usage"
ai "list all running services"
ai "show network connections"

# Questions
ai "what is uvx and where does it install files?"
ai "how do I configure SSH key authentication?"
ai "what's the difference between systemctl and service?"
ai "where are nginx configuration files located?"
ai "explain how Linux file permissions work"
```

### OS-Specific Command Generation
The tool automatically detects your operating system and generates appropriate commands:

```bash
# Check detected OS
ai --show-os

# Override OS detection (useful for remote administration)
ai --target-os linux-ubuntu "check system memory"
ai --target-os macos "list running services"
ai --target-os linux-centos "update packages"
```

**Supported Systems:**
- **macOS**: Uses `vm_stat`, `launchctl`, `brew`
- **Ubuntu/Debian**: Uses `free`, `systemctl`, `apt`
- **CentOS/RHEL**: Uses `free`, `systemctl`, `yum`
- **Arch Linux**: Uses `free`, `systemctl`, `pacman`
- **FreeBSD**: Uses `top`, `service`, `pkg`
- **Generic Unix/Linux**: Fallback commands

### Direct Execution
```bash
./sysadmin_ai.py --help
./sysadmin_ai.py --interactive
./sysadmin_ai.py "show disk usage"
```

### With Safety Options
```bash
ai --safe-mode "clean up temporary files"
ai --auto-confirm "show running services"
```

## Question & Answer Mode 🤔

The tool now intelligently detects when you're asking a question and provides detailed explanations with web search integration.

### Intelligent Intent Detection
Claude automatically determines whether you're asking a question or requesting commands - no special syntax needed! Just talk naturally and Claude will:
- **Provide explanations** for questions about concepts, tools, and configurations
- **Generate commands** for actionable requests like "show disk usage"

### Web Search Integration
Claude can search the web for current information when answering questions:
```bash
ai "what is the latest version of Docker?"
ai "how to install Node.js on Ubuntu 22.04?"
ai "what are the best practices for SSH security?"
```

### Configuration Options
```bash
# Configure settings (including web search)
ai --config

# Disable web search for answers
ai --disable-web-search "what is systemd?"
```

### Natural Language Examples

Claude automatically determines your intent - no special syntax needed:

**Questions** (Claude provides detailed explanations):
- "what is uvx and where does it install files?"
- "how do I configure SSH key authentication?"
- "what's the difference between apt and snap?"
- "where are log files typically stored?"
- "explain how cron jobs work"

**Commands** (Claude generates executable bash):
- "install docker" → `brew install docker` (macOS)
- "check disk usage" → `df -h`
- "find large files" → `find . -type f -size +100M`
- "restart nginx service" → `sudo systemctl restart nginx`
- "show running processes" → `ps aux`

## API Key Management 🔐

The tool supports multiple ways to provide your Anthropic API key:

### 1. Environment Variable (Recommended)
```bash
export ANTHROPIC_API_KEY="your_api_key_here"
./sysadmin-ai.py --interactive
```

### 2. Local .env.secrets File
Create a `.env.secrets` file in the sysadmin directory:
```
ANTHROPIC_API_KEY=your_api_key_here
```

### 3. Embedded Key (For Deployment)
For deploying to remote servers where environment setup is complex:

```bash
./sysadmin_ai.py --embed-key sysadmin-ai-embedded.py
```

This creates a version with an encrypted, embedded API key. You'll need to enter a passphrase when running it.

### 4. Interactive Prompt
If no key is found, the tool will prompt you to enter it securely.

## Deployment Options 📦

### Portable Package
Create a self-contained package for easy deployment:

```bash
./package-sysadmin-ai.py --portable sysadmin-ai-portable
cd sysadmin-ai-portable
./install.sh
```

### Standalone Script
Create a single file with bundled dependencies:

```bash
./package-sysadmin-ai.py --standalone sysadmin-ai-standalone.py
```

### Complete Package
Create both versions:

```bash
./package-sysadmin-ai.py --all
```

## Security Features 🛡️

### Safe Mode
Prevents execution of potentially dangerous commands:
- File system destruction (`rm -rf /`)
- Disk operations (`dd`, `mkfs`, `fdisk`)
- System shutdown commands
- Permission changes to system files

```bash
./sysadmin_ai.py --safe-mode --interactive
```

### Command Confirmation
Before executing commands, the tool shows:
- All commands to be executed
- Danger warnings for risky operations
- Options to edit, cancel, or proceed

### Command Validation
Built-in patterns detect dangerous operations:
- Root filesystem operations
- Bulk deletion commands
- System configuration changes
- Hardware manipulation commands


## Configuration ⚙️

### Interactive Configuration
Run `config` in interactive mode to modify settings:

```
sysadmin_ai> config
```

### Settings Available
- **Safe Mode**: Prevent dangerous command execution
- **Auto Confirm**: Automatically confirm safe commands
- **Log Commands**: Log all executed commands
- **Web Search**: Enable web search for answers (default: ON)
- **Model**: Claude model to use (default: claude-haiku-4-5-20251001)
- **Timeout**: Command execution timeout in seconds
- **Web Search Max Uses**: Maximum web searches Claude can perform per request (1-10)

### Configuration File
Settings are stored in `~/.sysadmin-ai.json`:

```json
{
  "model": "claude-haiku-4-5-20251001",
  "max_tokens": 1500,
  "auto_confirm": false,
  "log_commands": true,
  "safe_mode": true,
  "command_timeout": 300,
  "enable_web_search": true,
  "web_search_max_uses": 5,
}
```

## Common System Administration Tasks 💡

### Mixed Examples (Claude Determines Intent Automatically)
| Natural Language Input | Claude's Response |
|------------------------|-------------------|
| "show disk usage" | **Commands**: `df -h` |
| "what is uvx and where does it install files?" | **Explanation**: Detailed description of uvx tool, installation locations, and usage patterns |
| "find large files in /var/log" | **Commands**: `find /var/log -type f -size +100M -exec ls -lh {} \;` |
| "how do SSH keys work?" | **Explanation**: SSH key authentication process, generation, security benefits |
| "backup my home directory" | **Commands**: `tar -czf ~/backup-$(date +%Y%m%d).tar.gz ~` |
| "what's the difference between systemctl and service?" | **Explanation**: Comparison of systemd vs traditional service management |
| "check running processes" | **Commands**: `ps aux` |
| "where are nginx config files located?" | **Explanation**: Config file locations across different distributions |
| "restart apache service" | **Commands**: `sudo systemctl restart apache2` |
| "explain Linux file permissions" | **Explanation**: Permission system, chmod, chown, and practical examples |
| "show network connections" | **Commands**: `netstat -tuln` or `ss -tuln` |
| "what does the ps command do?" | **Explanation**: Process listing functionality and common options |
| "list all services" | **Commands**: `systemctl list-units --type=service` |
| "how do I set up a cron job?" | **Explanation**: Cron syntax, examples, and best practices |
| "update package lists" | **Commands**: `sudo apt update` (Debian/Ubuntu) or `brew update` (macOS) |
| "what is Docker and how does it work?" | **Explanation**: Containerization concepts and Docker basics |

## Advanced Features 🔧

### Command History
View recent commands:
```
sysadmin-ai> history
```

### Command Editing
When confirming commands, use 'e' to edit them before execution.

### Detailed Command Information
Use 's' during confirmation to see detailed information about commands.

### Logging
All executed commands are logged to `~/.sysadmin-ai.log` with timestamps.

## Installation Helper Scripts

The directory includes several helper scripts:

- **`install-uv.sh`** - Fast installation using uv (recommended, 10-100x faster than pip)
- **`install.sh`** - Traditional installation with pip and dependency management
- **`setup-alias.sh`** - Set up the `ai` alias for easy command access
- **`demo.sh`** - Demonstration script showing tool capabilities
- **`package-sysadmin-ai.py`** - Create portable/standalone distributions

### Manual Alias Setup

If you need to set up the alias manually:

```bash
# Run the alias setup script
./setup-alias.sh

# Or add manually to your shell config (~/.bashrc, ~/.zshrc, etc.)
alias ai='/path/to/sysadmin_ai.py'
```

## Troubleshooting 🔍

### Common Issues

**Can't find the `ai` command after installation?**
```bash
# Make sure your Python scripts directory is in PATH
# For pip user install:
export PATH="$HOME/.local/bin:$PATH"

# For system install, restart your terminal
```

**Slow pip installation?**
Use uv instead! It's 10-100x faster:
```bash
# Install with uv
uv pip install sysadmin-ai

# Or install uv first, then install the package
curl -LsSf https://astral.sh/uv/install.sh | sh
uv pip install sysadmin-ai
```

**pip3 not found during installation**
The installer will provide specific commands for your OS. Common solutions:
```bash
# macOS
brew install python

# Ubuntu/Debian
sudo apt update && sudo apt install python3-pip

# CentOS/RHEL
sudo yum install python3-pip

# Fedora
sudo dnf install python3-pip

# Arch Linux
sudo pacman -S python-pip
```

**uv not found after installation**
If uv was just installed, you may need to restart your shell or source the environment:
```bash
source $HOME/.cargo/env
# Or restart your terminal
```

**ImportError: No module named 'requests'**
```bash
pip install requests cryptography
# or if pip3 is available
pip3 install requests cryptography
```

**Permission errors during pip install**
Try installing with user flag or system-wide:
```bash
pip3 install -r requirements.txt --user
# or system-wide (requires sudo)
sudo pip3 install -r requirements.txt
```

**API Key Not Found**
- Check environment variable: `echo $ANTHROPIC_API_KEY`
- Verify .env.secrets file exists and has correct format
- Ensure no extra spaces or quotes in the key

**Permission Denied**
```bash
chmod +x sysadmin_ai.py
```

**Commands Not Working**
- Check if you're in safe mode (dangerous commands are blocked)
- Verify the translated command makes sense  
- Try being more specific in your natural language request
- Check detected OS with `ai --show-os`

**Alias not working after installation**
```bash
# Reload shell configuration
source ~/.bashrc        # Linux
source ~/.bash_profile  # macOS
source ~/.zshrc         # If using zsh

# Or start a new terminal session
```

### Debug Mode
For troubleshooting API issues, you can check the raw API responses by modifying the code temporarily or using verbose logging.

## Use Cases 🎯

Perfect for:
- **System Administrators** who want to work faster with natural language and get quick answers
- **DevOps Engineers** managing multiple servers and environments
- **Developers** who need occasional system administration tasks and explanations
- **Students** learning Unix/Linux system administration with interactive Q&A
- **Technical Support** answering user questions about system configurations
- **Documentation** creating explanations for system administration procedures
- **Remote Server Management** with embedded API key deployment
- **Automation Scripts** that need human-readable command descriptions
- **Training and Education** with explanatory answers and examples

## Development 🛠️

### Requirements
- Python 3.7+
- requests >= 2.31.0
- cryptography >= 41.0.0 (for embedded keys)

### Testing
Test the tool safely:

```bash
# Enable safe mode
./sysadmin_ai.py --safe-mode --interactive

# Test with harmless commands
"show current directory"
"list files in current directory"
"show system date and time"
```

### Contributing
- Improve command translation accuracy
- Add more safety patterns
- Enhance error handling
- Add support for other AI models

## Security Notice ⚠️

- Always review commands before execution
- Use safe mode in production environments
- Keep your API key secure
- Be cautious with embedded key deployments
- Regularly review command logs
- Test in non-production environments first

## Support 💬

For issues, feature requests, or questions:
- Review the troubleshooting section
- Check command logs in `~/.sysadmin-ai.log`
- Ensure your Anthropic API key is valid and has sufficient credits
- Verify network connectivity to api.anthropic.com
---

**Disclaimer**: This tool executes system commands based on AI interpretation of natural language. Always verify commands before execution and use appropriate safety measures in production environments.

## Quick Demo

Try running:
```bash
./demo.sh
```

This will show you the tool's capabilities and help you get started!

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
