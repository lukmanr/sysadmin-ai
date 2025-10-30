# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.1] - 2025-01-30

### Added
- PyPI installation as the recommended installation method
- PyPI version badge, Python version badge, and MIT license badge to README
- Comprehensive installation documentation for PyPI-based installation
- Quick test section in README for verifying installation
- Consolidated "Setting Up Your API Key" section in README
- Troubleshooting entry for PATH configuration issues

### Changed
- Reorganized installation options to prioritize PyPI installation
- Updated README to show `pip install sysadmin-ai` and `uv pip install sysadmin-ai` as primary installation methods
- Renamed source installation options to clarify they're for development
- Improved installation flow documentation

### Documentation
- Updated all installation examples to include PyPI method first
- Added git clone instructions for source-based installations
- Enhanced troubleshooting section with PyPI-specific guidance

## [1.0.0] - 2025-01-30

### Added
- Initial release on PyPI
- Natural language interface for Unix/Linux system administration
- Smart command translation using Claude AI (Haiku 4.5)
- Question & Answer mode with automatic intent detection
- Web search integration for up-to-date information
- OS-specific command generation (macOS, Ubuntu, Debian, CentOS, RHEL, Arch, FreeBSD)
- Interactive and single-command modes
- Safe mode with dangerous command detection
- Command confirmation and editing capabilities
- Command history and logging
- Configurable settings (safe mode, auto-confirm, web search, etc.)
- Multiple API key management options (environment variable, .env.secrets, embedded, interactive)
- `uv` support for fast package installation (10-100x faster than pip)
- Installation scripts for both pip and uv
- Alias setup script for easy `ai` command access
- Demo script showcasing tool capabilities
- Packaging utilities for creating portable and standalone distributions
- Embedded API key support with encryption
- MIT License

### Entry Points
- `sysadmin-ai` - Main command
- `ai` - Short alias command

### Dependencies
- Python 3.7+
- requests >= 2.31.0
- cryptography >= 41.0.0

### Documentation
- Comprehensive README with installation, usage, and troubleshooting
- UV installation guide
- Examples for common system administration tasks
- Security features documentation
- Configuration guide

[1.0.1]: https://github.com/lukmanr/sysadmin-ai/compare/v1.0.0...v1.0.1
[1.0.0]: https://github.com/lukmanr/sysadmin-ai/releases/tag/v1.0.0

