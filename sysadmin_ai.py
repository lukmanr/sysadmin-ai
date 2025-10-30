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
SysAdmin AI - Natural Language Unix/Linux System Administration Tool
A CLI tool for translating natural language to bash commands using Claude AI
Copyright (c) Lukman Ramsey 2025
"""

import os
import sys
import json
import subprocess
import argparse
import getpass
import hashlib
import base64
import platform
from pathlib import Path
from typing import Optional, List, Dict, Any
import re

# Try to import optional dependencies
try:
    import requests
except ImportError:
    print("Error: 'requests' library is required. Install with: pip install requests")
    sys.exit(1)

try:
    from cryptography.fernet import Fernet
    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False

# Version info
VERSION = "1.0.1"
TOOL_NAME = "SysAdmin AI"

# Configuration
DEFAULT_MODEL = "claude-haiku-4-5-20251001"
API_BASE_URL = "https://api.anthropic.com/v1/messages"
MAX_TOKENS = 1500
DANGEROUS_COMMANDS = [
    'rm -rf /', 'rm -rf /*', 'dd if=/dev/zero', 'mkfs', 'fdisk', 'parted',
    'shutdown', 'reboot', 'halt', 'poweroff', 'init 0', 'init 6',
    'chmod 000', 'chown root:root /', 'mv /* /dev/null', 'cat /dev/urandom',
    ':(){ :|:& };:', 'sudo rm -rf', 'rm -rf ~', 'rm -rf $HOME'
]

# Web search tool configuration
WEB_SEARCH_MAX_USES = 5

# Embedded encrypted API key placeholder (will be replaced by packaging script)
EMBEDDED_KEY = None  # EMBEDDED_KEY_PLACEHOLDER

class SysAdminAI:
    def __init__(self, target_os=None):
        self.api_key = None
        self.session_id = None
        self.command_history = []
        self.target_os = target_os or self.detect_os()
        self.config = self.load_config()
        
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from file or create default"""
        config_file = Path.home() / '.sysadmin-ai.json'
        default_config = {
            'model': DEFAULT_MODEL,
            'max_tokens': MAX_TOKENS,
            'auto_confirm': False,
            'log_commands': True,
            'safe_mode': True,
            'command_timeout': 300,
            'enable_web_search': True,
            'web_search_max_uses': 5,
        }
        
        if config_file.exists():
            try:
                with open(config_file, 'r') as f:
                    config = json.load(f)
                # Merge with defaults for any missing keys
                for key, value in default_config.items():
                    if key not in config:
                        config[key] = value
                return config
            except Exception as e:
                print(f"Warning: Failed to load config: {e}")
                
        return default_config
    
    def detect_os(self) -> str:
        """Detect the operating system and distribution"""
        system = platform.system().lower()
        
        if system == 'darwin':
            return 'macos'
        elif system == 'linux':
            # Try to detect Linux distribution
            try:
                # Check /etc/os-release
                if os.path.exists('/etc/os-release'):
                    with open('/etc/os-release', 'r') as f:
                        for line in f:
                            if line.startswith('ID='):
                                distro = line.split('=')[1].strip().strip('"\'')
                                return f'linux-{distro}'
                
                # Fallback: check for specific distribution files
                if os.path.exists('/etc/redhat-release'):
                    return 'linux-rhel'
                elif os.path.exists('/etc/debian_version'):
                    return 'linux-debian'
                elif os.path.exists('/etc/arch-release'):
                    return 'linux-arch'
                else:
                    return 'linux-generic'
            except Exception:
                return 'linux-generic'
        elif system in ['freebsd', 'openbsd', 'netbsd']:
            return system
        else:
            return 'unix-generic'
    
    def get_os_specific_info(self) -> Dict[str, str]:
        """Get OS-specific command information"""
        os_info = {
            'macos': {
                'memory_cmd': 'vm_stat',
                'process_cmd': 'ps aux',
                'network_cmd': 'netstat -rn',
                'disk_cmd': 'df -h',
                'service_cmd': 'launchctl list',
                'package_manager': 'brew',
                'user_add': 'dscl . create',
                'description': 'macOS (Darwin)'
            },
            'linux-ubuntu': {
                'memory_cmd': 'free -h',
                'process_cmd': 'ps aux',
                'network_cmd': 'ss -tuln',
                'disk_cmd': 'df -h',
                'service_cmd': 'systemctl',
                'package_manager': 'apt',
                'user_add': 'useradd',
                'description': 'Ubuntu Linux'
            },
            'linux-debian': {
                'memory_cmd': 'free -h',
                'process_cmd': 'ps aux',
                'network_cmd': 'ss -tuln',
                'disk_cmd': 'df -h',
                'service_cmd': 'systemctl',
                'package_manager': 'apt',
                'user_add': 'useradd',
                'description': 'Debian Linux'
            },
            'linux-centos': {
                'memory_cmd': 'free -h',
                'process_cmd': 'ps aux',
                'network_cmd': 'ss -tuln',
                'disk_cmd': 'df -h',
                'service_cmd': 'systemctl',
                'package_manager': 'yum',
                'user_add': 'useradd',
                'description': 'CentOS Linux'
            },
            'linux-rhel': {
                'memory_cmd': 'free -h',
                'process_cmd': 'ps aux',
                'network_cmd': 'ss -tuln',
                'disk_cmd': 'df -h',
                'service_cmd': 'systemctl',
                'package_manager': 'yum',
                'user_add': 'useradd',
                'description': 'Red Hat Enterprise Linux'
            },
            'linux-arch': {
                'memory_cmd': 'free -h',
                'process_cmd': 'ps aux',
                'network_cmd': 'ss -tuln',
                'disk_cmd': 'df -h',
                'service_cmd': 'systemctl',
                'package_manager': 'pacman',
                'user_add': 'useradd',
                'description': 'Arch Linux'
            },
            'linux-generic': {
                'memory_cmd': 'free -h',
                'process_cmd': 'ps aux',
                'network_cmd': 'netstat -tuln',
                'disk_cmd': 'df -h',
                'service_cmd': 'service',
                'package_manager': 'package manager',
                'user_add': 'useradd',
                'description': 'Generic Linux'
            },
            'freebsd': {
                'memory_cmd': 'top -n 1',
                'process_cmd': 'ps aux',
                'network_cmd': 'netstat -rn',
                'disk_cmd': 'df -h',
                'service_cmd': 'service',
                'package_manager': 'pkg',
                'user_add': 'pw useradd',
                'description': 'FreeBSD'
            },
            'unix-generic': {
                'memory_cmd': 'top -n 1',
                'process_cmd': 'ps aux',
                'network_cmd': 'netstat -tuln',
                'disk_cmd': 'df -h',
                'service_cmd': 'service',
                'package_manager': 'package manager',
                'user_add': 'adduser',
                'description': 'Generic Unix'
            }
        }
        
        return os_info.get(self.target_os, os_info['unix-generic'])
    
    def save_config(self):
        """Save current configuration"""
        config_file = Path.home() / '.sysadmin-ai.json'
        try:
            with open(config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            print(f"Warning: Failed to save config: {e}")
    
    def get_api_key(self) -> str:
        """Get API key from various sources in order of preference"""
        # 1. Environment variable
        if 'ANTHROPIC_API_KEY' in os.environ:
            return os.environ['ANTHROPIC_API_KEY']
        
        # 2. Local .env.secrets file
        env_file = Path('.env.secrets')
        if env_file.exists():
            try:
                with open(env_file, 'r') as f:
                    for line in f:
                        if line.startswith('ANTHROPIC_API_KEY='):
                            return line.split('=', 1)[1].strip().strip('"\'')
            except Exception as e:
                print(f"Warning: Failed to read .env.secrets: {e}")
        
        # 3. Embedded key (if available and crypto is available)
        if EMBEDDED_KEY and CRYPTO_AVAILABLE:
            try:
                # Prompt for passphrase to decrypt embedded key
                passphrase = getpass.getpass("Enter passphrase for embedded API key: ")
                key = self.derive_key_from_passphrase(passphrase)
                fernet = Fernet(key)
                return fernet.decrypt(base64.b64decode(EMBEDDED_KEY)).decode()
            except Exception as e:
                print(f"Failed to decrypt embedded key: {e}")
        
        # 4. Prompt user
        return getpass.getpass("Enter Anthropic API key: ")
    
    def derive_key_from_passphrase(self, passphrase: str) -> bytes:
        """Derive encryption key from passphrase"""
        return base64.urlsafe_b64encode(hashlib.pbkdf2_hmac(
            'sha256', passphrase.encode(), b'sysadmin-ai-salt', 100000
        )[:32])
        
    def process_with_claude(self, user_input: str) -> Dict[str, Any]:
        """Process user input with Claude, letting it determine whether to answer or generate commands"""
        if not self.api_key:
            self.api_key = self.get_api_key()
        
        # Get OS-specific information
        os_info = self.get_os_specific_info()
        
        # System prompt that handles both questions and commands
        system_prompt = f"""You are a Unix/Linux system administration expert assistant with access to advanced educational and content management tools. You can help users in three ways:

1. ANSWER QUESTIONS: When users ask questions about Unix/Linux systems, tools, concepts, or administration, provide detailed, helpful explanations.

2. GENERATE COMMANDS: When users request actions to be performed, generate the appropriate bash commands for their system.

Your target system: {os_info['description']}

For QUESTIONS (like "what is docker?", "how does SSH work?", "where are config files?"):
- Provide detailed explanations in clear English
- Include practical examples and file locations
- Mention OS-specific differences when relevant
- If you need current information, use web search
- Be specific about configuration files and system behavior

For COMMAND REQUESTS (like "show disk usage", "find large files", "restart service", "set git remote"):
- Return ONLY the executable commands, one per line
- ABSOLUTELY NO explanations, comments, descriptions, or introductory text
- NEVER include phrases like "Since this is a command request" or "I'll provide the exact command"
- NEVER include markdown formatting, backticks, or code blocks
- Just the raw commands that can be executed directly
- Use commands that work specifically on {os_info['description']}
- Be precise and safe - avoid destructive operations unless explicitly requested
- Use appropriate flags for safety (e.g., -i for interactive, -v for verbose)

CRITICAL: If the user is requesting an action (not asking a question), respond with ONLY the commands. No explanatory text whatsoever.

OS-Specific Command Guidelines for {os_info['description']}:
- Memory information: {os_info['memory_cmd']}
- Process listing: {os_info['process_cmd']}
- Network information: {os_info['network_cmd']}
- Disk usage: {os_info['disk_cmd']}
- Service management: {os_info['service_cmd']}
- Package management: {os_info['package_manager']}
- User management: {os_info['user_add']}

Examples:
User: "what is uvx and where does it install files?"
Response: [Detailed explanation about uvx, installation locations, usage]

User: "show disk usage"
Response: {os_info['disk_cmd']}

User: "set origin remote URL to git@github.com:user/repo.git"
Response: git remote set-url origin git@github.com:user/repo.git

Determine the user's intent and respond appropriately."""

        headers = {
            'x-api-key': self.api_key,
            'content-type': 'application/json',
            'anthropic-version': '2023-06-01'
        }
        
        # Prepare tools array
        tools = []
        if self.config.get('enable_web_search', True):
            tools.append({
                "type": "web_search_20250305",
                "name": "web_search",
                "max_uses": self.config.get('web_search_max_uses', 5)
            })
        
        data = {
            'model': self.config['model'],
            'max_tokens': self.config['max_tokens'],
            'system': system_prompt,
            'messages': [
                {
                    'role': 'user',
                    'content': user_input
                }
            ]
        }
        
        # Add tools if web search is enabled
        if tools:
            data['tools'] = tools
        
        try:
            #print("params:", API_BASE_URL, headers, data)
            response = requests.post(API_BASE_URL, headers=headers, json=data, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            
            # Extract the final text content
            content = ""
            for content_block in result['content']:
                if content_block['type'] == 'text':
                    content += content_block['text']
            
            # Determine if this looks like commands or an explanation
            lines = [line.strip() for line in content.strip().split('\n') if line.strip()]
            
            # Extract potential commands by filtering out explanatory lines
            potential_commands = []
            explanatory_lines = []
            
            for line in lines:
                line_lower = line.lower()
                # Skip lines that are clearly explanatory
                if (line.startswith('#') or 
                    any(phrase in line_lower for phrase in [
                        'since this is', 'i\'ll provide', 'here is', 'here are', 
                        'this command', 'the command', 'explanation:', 'note:',
                        'to do this', 'you can use', 'this will', 'the following'
                    ]) or
                    line.endswith(':') or
                    len(line) > 300):  # Very long lines are likely explanations
                    explanatory_lines.append(line)
                else:
                    # Check if line looks like a command (starts with common command patterns)
                    if (line and not line[0].isupper() and 
                        (any(line.startswith(cmd) for cmd in [
                            'git ', 'ls ', 'cd ', 'mkdir ', 'rm ', 'cp ', 'mv ', 'chmod ', 'chown ',
                            'sudo ', 'apt ', 'yum ', 'brew ', 'pip ', 'npm ', 'docker ', 'systemctl ',
                            'service ', 'ps ', 'top ', 'df ', 'du ', 'find ', 'grep ', 'awk ', 'sed ',
                            'tar ', 'gzip ', 'curl ', 'wget ', 'ssh ', 'scp ', 'rsync ', 'cat ', 'less ',
                            'tail ', 'head ', 'sort ', 'uniq ', 'wc ', 'which ', 'whereis ', 'locate ',
                            'mount ', 'umount ', 'fdisk ', 'lsblk ', 'free ', 'vmstat ', 'netstat ',
                            'ss ', 'iptables ', 'ufw ', 'firewall-cmd ', 'crontab ', 'at ', 'nohup '
                        ]) or 
                        '|' in line or  # Pipes suggest commands
                        line.startswith('./') or  # Script execution
                        line.startswith('~/'))):  # Home directory paths
                        potential_commands.append(line)
                    else:
                        explanatory_lines.append(line)
            
            # Determine if this is primarily commands or explanation
            if potential_commands and len(potential_commands) >= len(explanatory_lines):
                # More command-like lines than explanatory lines
                return {
                    'type': 'commands',
                    'content': content.strip(),
                    'lines': potential_commands
                }
            else:
                # Primarily explanatory content
                return {
                    'type': 'explanation',
                    'content': content.strip(),
                    'lines': [content.strip()]
                }
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"API request failed: {e}")
        except Exception as e:
            raise Exception(f"Failed to process request: {e}")
    
    def translate_to_commands(self, natural_language: str) -> List[str]:
        """Translate natural language to bash commands using Claude API"""
        if not self.api_key:
            self.api_key = self.get_api_key()
        
        # Get OS-specific information
        os_info = self.get_os_specific_info()
        
        # System prompt for command translation
        system_prompt = f"""You are a Unix/Linux system administration expert. Translate natural language requests into appropriate bash commands for {os_info['description']}.

Rules:
1. Return ONLY the commands, one per line
2. No explanations, comments, or markdown formatting  
3. Use commands that work specifically on {os_info['description']}
4. Be precise and safe - avoid destructive operations unless explicitly requested
5. If multiple commands are needed, separate them with newlines
6. For complex operations, break into logical steps
7. Always use appropriate flags and options for safety (e.g., -i for interactive, -v for verbose when appropriate)
8. If the request is unclear or potentially dangerous, suggest a safer alternative

OS-Specific Command Guidelines for {os_info['description']}:
- Memory information: {os_info['memory_cmd']}
- Process listing: {os_info['process_cmd']}
- Network information: {os_info['network_cmd']}
- Disk usage: {os_info['disk_cmd']}
- Service management: {os_info['service_cmd']}
- Package management: {os_info['package_manager']}
- User management: {os_info['user_add']}

Examples for {os_info['description']}:
User: "show me disk usage"
Response: {os_info['disk_cmd']}

User: "check system memory"
Response: {os_info['memory_cmd']}

User: "find large files in /var/log"
Response: find /var/log -type f -size +100M -exec ls -lh {{}} \;

User: "backup my home directory"
Response: tar -czf ~/backup-$(date +%Y%m%d).tar.gz ~

Current system: {os_info['description']}"""

        headers = {
            'x-api-key': self.api_key,
            'content-type': 'application/json',
            'anthropic-version': '2023-06-01'
        }
        
        data = {
            'model': self.config['model'],
            'max_tokens': self.config['max_tokens'],
            'system': system_prompt,
            'messages': [
                {
                    'role': 'user',
                    'content': natural_language
                }
            ]
        }
        
        try:
            response = requests.post(API_BASE_URL, headers=headers, json=data, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            content = result['content'][0]['text'].strip()
            
            # Parse commands from response
            commands = [cmd.strip() for cmd in content.split('\n') if cmd.strip()]
            return commands
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"API request failed: {e}")
        except Exception as e:
            raise Exception(f"Failed to translate command: {e}")
    
    def is_dangerous_command(self, command: str) -> bool:
        """Check if command is potentially dangerous"""
        command_lower = command.lower().strip()
        
        # Check against known dangerous patterns
        for dangerous in DANGEROUS_COMMANDS:
            if dangerous in command_lower:
                return True
        
        # Additional heuristic checks
        dangerous_patterns = [
            r'rm\s+-rf?\s+/\w*\s*$',  # rm -rf /something or rm -rf /
            r'dd\s+if=/dev/(zero|urandom)',  # dd with dangerous sources
            r'sudo\s+rm\s+-rf',  # sudo rm -rf
            r'chmod\s+000',  # chmod 000
            r'>\s*/dev/sd[a-z]',  # Writing to disk devices
            r'mkfs\.',  # Making filesystems
            r'fdisk|parted',  # Disk partitioning
        ]
        
        for pattern in dangerous_patterns:
            if re.search(pattern, command_lower):
                return True
        
        return False
    
    def confirm_execution(self, commands: List[str]) -> bool:
        """Ask user to confirm command execution"""
        print("\n" + "="*60)
        print("Commands to execute:")
        print("="*60)
        
        for i, cmd in enumerate(commands, 1):
            danger_flag = " ⚠️  DANGEROUS" if self.is_dangerous_command(cmd) else ""
            print(f"{i:2d}. {cmd}{danger_flag}")
        
        print("="*60)
        
        if self.config['auto_confirm'] and not any(self.is_dangerous_command(cmd) for cmd in commands):
            print("Auto-confirming safe commands...")
            return True
        
        while True:
            response = input("\nExecute these commands? [y/N/e/s]: ").lower().strip()
            if response in ['y', 'yes']:
                return True
            elif response in ['n', 'no', '']:
                return False
            elif response in ['e', 'edit']:
                return self.edit_commands(commands)
            elif response in ['s', 'show']:
                self.show_command_details(commands)
            else:
                print("Options: y=yes, n=no, e=edit, s=show details")
    
    def edit_commands(self, commands: List[str]) -> bool:
        """Allow user to edit commands before execution"""
        print("\nEditing commands (empty line to finish):")
        edited_commands = []
        
        for i, cmd in enumerate(commands):
            new_cmd = input(f"Command {i+1} [{cmd}]: ").strip()
            if new_cmd:
                edited_commands.append(new_cmd)
            else:
                edited_commands.append(cmd)
        
        # Allow adding new commands
        print("Add additional commands (empty line to finish):")
        while True:
            new_cmd = input("Additional command: ").strip()
            if not new_cmd:
                break
            edited_commands.append(new_cmd)
        
        return self.confirm_execution(edited_commands)
    
    def show_command_details(self, commands: List[str]):
        """Show detailed information about commands"""
        print("\nCommand details:")
        for i, cmd in enumerate(commands, 1):
            print(f"\n{i}. {cmd}")
            if self.is_dangerous_command(cmd):
                print("   ⚠️  WARNING: This command is potentially dangerous!")
            
            # Try to show man page summary
            try:
                main_cmd = cmd.split()[0]
                result = subprocess.run(['whatis', main_cmd], 
                                      capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    print(f"   Description: {result.stdout.strip()}")
            except:
                pass
    
    def execute_commands(self, commands: List[str]) -> bool:
        """Execute the commands with proper logging and error handling"""
        success_count = 0
        
        for i, command in enumerate(commands, 1):
            print(f"\n[{i}/{len(commands)}] Executing: {command}")
            
            if self.config['safe_mode'] and self.is_dangerous_command(command):
                print("⚠️  Skipping dangerous command in safe mode")
                continue
            
            try:
                # Log command if enabled
                if self.config['log_commands']:
                    self.log_command(command)
                
                # Execute command
                result = subprocess.run(
                    command, 
                    shell=True, 
                    timeout=self.config['command_timeout'],
                    text=True
                )
                
                if result.returncode == 0:
                    print(f"✅ Command {i} completed successfully")
                    success_count += 1
                else:
                    print(f"❌ Command {i} failed with exit code {result.returncode}")
                
            except subprocess.TimeoutExpired:
                print(f"⏰ Command {i} timed out after {self.config['command_timeout']} seconds")
            except Exception as e:
                print(f"❌ Command {i} failed: {e}")
        
        print(f"\nExecution summary: {success_count}/{len(commands)} commands succeeded")
        return success_count == len(commands)
    
    def log_command(self, command: str):
        """Log executed command to file"""
        log_file = Path.home() / '.sysadmin-ai.log'
        try:
            with open(log_file, 'a') as f:
                timestamp = subprocess.check_output(['date'], text=True).strip()
                f.write(f"{timestamp}: {command}\n")
        except Exception as e:
            print(f"Warning: Failed to log command: {e}")
    
    def interactive_mode(self):
        """Run in interactive mode"""
        print(f"{TOOL_NAME} v{VERSION} - Interactive Mode")
        print("Type 'quit', 'exit', or 'q' to exit")
        print("Type 'help' for available commands")
        print("Type 'config' to modify settings")
        print("")
                
        print("💡 Just talk naturally:")
        print("   • Ask questions: 'what is docker?' or 'where does pip install packages?'")
        print("   • Request commands: 'show disk usage' or 'find large files'")
        print("   • Claude will determine your intent automatically")
        if self.config.get('enable_web_search', True):
            print("   • Web search is enabled for current information")
        print("-" * 50)
        
        while True:
            try:
                user_input = input("\nsysadmin-ai> ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("Goodbye!")
                    break
                
                if user_input.lower() == 'help':
                    self.show_help()
                    continue
                
                if user_input.lower() == 'config':
                    self.configure_settings()
                    continue
                
                if user_input.lower() == 'history':
                    self.show_history()
                    continue
                                
                # Translate and execute
                self.process_request(user_input)
                
            except KeyboardInterrupt:
                print("\nInterrupted by user")
                break
            except EOFError:
                print("\nGoodbye!")
                break
    
    def process_request(self, request: str):
        """Process a single natural language request using Claude to determine intent"""
        try:
            print(f"Processing: {request}")
            if self.config.get('enable_web_search', True):
                print("🔍 Web search available if needed...")

            # process request with Claude
            result = self.process_with_claude(request)
            
            if result['type'] == 'commands':
                # Claude determined this is a command request
                commands = result['lines']
                
                if not commands:
                    print("No commands generated from your request.")
                    return
                
                self.command_history.extend(commands)
                
                if self.confirm_execution(commands):
                    self.execute_commands(commands)
                else:
                    print("Command execution cancelled.")
                
            else:
                # Claude determined this is a question and provided an explanation
                print("\n" + "="*60)
                print("Answer:")
                print("="*60)
                print(result['content'])
                print("="*60)
                
        except Exception as e:
            print(f"Error: {e}")
    
    def show_help(self):
        """Show help information"""
        os_info = self.get_os_specific_info()
        print(f"""
{TOOL_NAME} v{VERSION} - Help

Detected System: {os_info['description']} (target_os: {self.target_os})

Commands:
  help     - Show this help
  config   - Configure settings
  history  - Show command history
  quit/exit/q - Exit the program

Settings:
  Safe Mode: {'ON' if self.config['safe_mode'] else 'OFF'} - Prevents execution of dangerous commands
  Auto Confirm: {'ON' if self.config['auto_confirm'] else 'OFF'} - Auto-confirm safe commands
  Log Commands: {'ON' if self.config['log_commands'] else 'OFF'} - Log all executed commands
  Web Search: {'ON' if self.config.get('enable_web_search', True) else 'OFF'} - Enable web search for answers
  Model: {self.config['model']}
  Timeout: {self.config['command_timeout']} seconds

OS-Specific Commands for {os_info['description']}:
  Memory: {os_info['memory_cmd']}
  Processes: {os_info['process_cmd']}
  Network: {os_info['network_cmd']}
  Disk: {os_info['disk_cmd']}
  Services: {os_info['service_cmd']}
  Packages: {os_info['package_manager']}

Natural Language Examples:
  "show disk usage" - generates: df -h
  "what is uvx and where does it install files?" - explains uvx tool
  "check system memory" - generates: vm_stat (macOS)
  "how do I configure SSH key authentication?" - explains SSH setup
  "find large files in /tmp" - generates: find command
  "what's the difference between systemctl and service?" - explains both
  "backup my home directory" - generates: tar command
  "where are nginx configuration files located?" - explains config locations
  "update the system packages" - generates: brew update (macOS)
  "explain how Linux file permissions work" - detailed explanation

""")
    
    def show_history(self):
        """Show command history"""
        if not self.command_history:
            print("No commands in history.")
            return
        
        print("Command History:")
        for i, cmd in enumerate(self.command_history[-10:], 1):  # Show last 10
            print(f"{i:2d}. {cmd}")
    
    def configure_settings(self):
        """Interactive configuration"""
        print("Configuration:")
        print(f"1. Safe Mode: {'ON' if self.config['safe_mode'] else 'OFF'}")
        print(f"2. Auto Confirm: {'ON' if self.config['auto_confirm'] else 'OFF'}")
        print(f"3. Log Commands: {'ON' if self.config['log_commands'] else 'OFF'}")
        print(f"4. Web Search: {'ON' if self.config.get('enable_web_search', True) else 'OFF'}")
        print(f"5. Model: {self.config['model']}")
        print(f"6. Timeout: {self.config['command_timeout']} seconds")
        print(f"7. Web Search Max Uses: {self.config.get('web_search_max_uses', 5)}")
        
        while True:
            choice = input("\nSelect option to change (1-7) or 'done': ").strip()
            
            if choice.lower() == 'done':
                break
            elif choice == '1':
                self.config['safe_mode'] = not self.config['safe_mode']
                print(f"Safe Mode: {'ON' if self.config['safe_mode'] else 'OFF'}")
            elif choice == '2':
                self.config['auto_confirm'] = not self.config['auto_confirm']
                print(f"Auto Confirm: {'ON' if self.config['auto_confirm'] else 'OFF'}")
            elif choice == '3':
                self.config['log_commands'] = not self.config['log_commands']
                print(f"Log Commands: {'ON' if self.config['log_commands'] else 'OFF'}")
            elif choice == '4':
                self.config['enable_web_search'] = not self.config.get('enable_web_search', True)
                print(f"Web Search: {'ON' if self.config['enable_web_search'] else 'OFF'}")
            elif choice == '5':
                new_model = input(f"Enter model [{self.config['model']}]: ").strip()
                if new_model:
                    self.config['model'] = new_model
            elif choice == '6':
                try:
                    new_timeout = int(input(f"Enter timeout in seconds [{self.config['command_timeout']}]: "))
                    self.config['command_timeout'] = new_timeout
                except ValueError:
                    print("Invalid timeout value")
            elif choice == '7':
                try:
                    new_uses = int(input(f"Enter max web search uses [1-10, current: {self.config.get('web_search_max_uses', 5)}]: "))
                    if 1 <= new_uses <= 10:
                        self.config['web_search_max_uses'] = new_uses
                        print(f"Web Search Max Uses: {new_uses}")
                    else:
                        print("Invalid value. Must be between 1 and 10.")
                except ValueError:
                    print("Invalid number")
        
        self.save_config()
        print("Configuration saved.")
        

def create_embedded_version(api_key: str, passphrase: str, output_file: str):
    """Create a version with embedded encrypted API key"""
    if not CRYPTO_AVAILABLE:
        print("Error: cryptography library required for embedded keys. Install with: pip install cryptography")
        return False
    
    # Derive key from passphrase
    key = base64.urlsafe_b64encode(hashlib.pbkdf2_hmac(
        'sha256', passphrase.encode(), b'sysadmin-ai-salt', 100000
    )[:32])
    
    # Encrypt API key
    fernet = Fernet(key)
    encrypted_key = base64.b64encode(fernet.encrypt(api_key.encode())).decode()
    
    # Read current script
    with open(__file__, 'r') as f:
        script_content = f.read()
    
    # Replace placeholder with encrypted key
    new_content = script_content.replace(
        'EMBEDDED_KEY = None  # EMBEDDED_KEY_PLACEHOLDER',
        f'EMBEDDED_KEY = "{encrypted_key}"'
    )
    
    # Write new script
    with open(output_file, 'w') as f:
        f.write(new_content)
    
    # Make executable
    os.chmod(output_file, 0o755)
    
    print(f"Created embedded version: {output_file}")
    print(f"The passphrase will be required when running the tool.")
    return True

def main():
    parser = argparse.ArgumentParser(description='SysAdmin AI - Natural Language Unix/Linux Administration with Q&A')
    parser.add_argument('command', nargs='*', help='Natural language command to execute or question to ask')
    parser.add_argument('--version', action='version', version=f'{TOOL_NAME} v{VERSION}')
    parser.add_argument('--interactive', '-i', action='store_true', help='Run in interactive mode')
    parser.add_argument('--config', action='store_true', help='Configure settings')
    parser.add_argument('--embed-key', metavar='OUTPUT_FILE', help='Create version with embedded API key')
    parser.add_argument('--safe-mode', action='store_true', help='Enable safe mode (prevent dangerous commands)')
    parser.add_argument('--auto-confirm', action='store_true', help='Auto-confirm safe commands')
    parser.add_argument('--disable-web-search', action='store_true', help='Disable web search for answers')
    parser.add_argument('--target-os', help='Target OS/distribution (e.g., macos, linux-ubuntu, linux-centos)')
    parser.add_argument('--show-os', action='store_true', help='Show detected OS and exit')
    
    args = parser.parse_args()
    
    # Handle show OS option
    if args.show_os:
        temp_tool = SysAdminAI(target_os=args.target_os)
        os_info = temp_tool.get_os_specific_info()
        print(f"Detected OS: {temp_tool.target_os}")
        print(f"Description: {os_info['description']}")
        print(f"Memory command: {os_info['memory_cmd']}")
        print(f"Process command: {os_info['process_cmd']}")
        print(f"Network command: {os_info['network_cmd']}")
        print(f"Package manager: {os_info['package_manager']}")
        sys.exit(0)
    
    # Handle embedded key creation
    if args.embed_key:
        api_key = getpass.getpass("Enter Anthropic API key to embed: ")
        passphrase = getpass.getpass("Enter passphrase for encryption: ")
        passphrase_confirm = getpass.getpass("Confirm passphrase: ")
        
        if passphrase != passphrase_confirm:
            print("Error: Passphrases don't match")
            sys.exit(1)
        
        if create_embedded_version(api_key, passphrase, args.embed_key):
            sys.exit(0)
        else:
            sys.exit(1)
    
    # Create tool instance
    tool = SysAdminAI(target_os=args.target_os)
    
    # Apply command line options
    if args.safe_mode:
        tool.config['safe_mode'] = True
    if args.auto_confirm:
        tool.config['auto_confirm'] = True
    if args.disable_web_search:
        tool.config['enable_web_search'] = False
    
    # Handle configuration mode
    if args.config:
        tool.configure_settings()
        sys.exit(0)
    
    # Handle interactive mode
    if args.interactive or not args.command:
        tool.interactive_mode()
        sys.exit(0)
    
    command_text = ' '.join(args.command)
    tool.process_request(command_text)

if __name__ == "__main__":
    main()
