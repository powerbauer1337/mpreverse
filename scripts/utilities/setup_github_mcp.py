#!/usr/bin/env python3
"""
GitHub MCP Server Setup Script
Uses the GitHub MCP server to create a repository and push the MarsPro project
"""

import asyncio
import json
import sys
import os
from pathlib import Path
from typing import Dict, Any

# Add the project root to the path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

async def setup_github_repository():
    """Set up GitHub repository using MCP GitHub server"""
    
    print("🚀 Setting up GitHub repository using MCP GitHub server...")
    
    # Repository configuration
    repo_config = {
        "name": "marspro-analysis",
        "description": "MarsPro reverse engineering and Home Assistant integration for local device control without cloud dependency",
        "private": False,
        "topics": [
            "home-assistant",
            "reverse-engineering", 
            "ble",
            "iot",
            "smart-home",
            "python",
            "marspro",
            "frida",
            "apk-analysis"
        ],
        "homepage": "",
        "has_issues": True,
        "has_projects": True,
        "has_wiki": True,
        "auto_init": False  # We'll push existing code
    }
    
    print(f"📋 Repository configuration:")
    print(f"   Name: {repo_config['name']}")
    print(f"   Description: {repo_config['description']}")
    print(f"   Private: {repo_config['private']}")
    print(f"   Topics: {', '.join(repo_config['topics'])}")
    
    # Note: The actual MCP GitHub server integration would be handled by Cursor
    # This script provides the configuration and instructions
    
    print("\n📝 Next steps:")
    print("1. Ensure you have a GitHub personal access token with repo permissions")
    print("2. The GitHub MCP server is now configured in config/mcp.json")
    print("3. Use Cursor's MCP integration to:")
    print("   - Create the repository")
    print("   - Push the code")
    print("   - Set up repository settings")
    
    print("\n🔧 Manual steps if needed:")
    print("1. Create repository on GitHub.com")
    print("2. Update the remote URL:")
    print("   git remote set-url origin https://github.com/YOUR_USERNAME/marspro-analysis.git")
    print("3. Push the code:")
    print("   git push -u origin main")
    
    return repo_config

async def create_release():
    """Create a GitHub release for the project"""
    
    release_config = {
        "tag_name": "v1.0.0",
        "name": "Initial Release - Project Reorganization Complete",
        "body": """# MarsPro Analysis v1.0.0

## 🎉 Initial Release

This release marks the completion of the major project reorganization and modernization of the MarsPro reverse engineering project.

### ✨ What's New

- **Modern Project Structure**: Reorganized with clear separation of concerns
- **Source Code Organization**: Moved to `src/` directory (Home Assistant + Review Gate)
- **Asset Management**: Organized APKs, tools, and extensions in `assets/` directory
- **Configuration Centralization**: All configs in `config/` directory
- **Tool Consolidation**: MCP servers and external tools properly organized
- **Comprehensive Testing**: Full test suite with unit and integration tests
- **Modern Python Packaging**: Added `pyproject.toml` and proper dependency management
- **Code Quality Tools**: Black, flake8, mypy, and pre-commit hooks
- **Enhanced Documentation**: Updated README and project structure docs

### 🏗️ Project Structure

```
MarsPro/
├── src/                    # Source code (Home Assistant + Review Gate)
├── assets/                 # Static assets (APKs, tools, extensions)
├── config/                 # Configuration files
├── tools/                  # Analysis tools and MCP servers
├── tests/                  # Comprehensive test suite
├── scripts/                # Automation scripts
├── analysis/               # Analysis documentation
└── output/                 # Analysis output files
```

### 🚀 Features

- **Home Assistant Integration**: Local control of MarsPro devices
- **BLE Communication**: Direct Bluetooth Low Energy communication
- **Cloud API Support**: Fallback to cloud API when needed
- **Analysis Tools**: Frida scripts and utilities for protocol discovery
- **MCP Server Integration**: Review Gate V2 and analysis tools
- **Modern Development**: Professional Python project standards

### 📋 Requirements

- Python 3.8+
- Home Assistant 2024.1+
- Git
- Android device with MarsPro app (for dynamic analysis)

### 🔧 Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/marspro-analysis.git
cd marspro-analysis

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Install Home Assistant integration
cp -r src/marspro /path/to/homeassistant/config/custom_components/
```

### 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html
```

### 📚 Documentation

- [README.md](README.md) - Project overview and setup guide
- [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) - Detailed project structure
- [REORGANIZATION_SUMMARY.md](REORGANIZATION_SUMMARY.md) - Reorganization details
- [CONTRIBUTING.md](CONTRIBUTING.md) - Contribution guidelines

### 🔮 Next Steps

- Phase 2: Dynamic analysis with Frida hooks
- Protocol discovery and documentation
- Enhanced Home Assistant integration
- Community contributions and feedback

### 🙏 Acknowledgments

- MarsPro team for creating the original app
- Home Assistant community for integration patterns
- Frida team for dynamic analysis tools
- JADX team for APK decompilation tools

---

**Note**: This project is for educational and research purposes. Please respect the terms of service of the original MarsPro application and use this integration responsibly.
""",
        "draft": False,
        "prerelease": False
    }
    
    print(f"\n📦 Release configuration:")
    print(f"   Tag: {release_config['tag_name']}")
    print(f"   Name: {release_config['name']}")
    print(f"   Draft: {release_config['draft']}")
    print(f"   Prerelease: {release_config['prerelease']}")
    
    return release_config

async def main():
    """Main function to set up GitHub repository"""
    
    print("🎯 MarsPro GitHub Repository Setup")
    print("=" * 50)
    
    # Set up repository configuration
    repo_config = await setup_github_repository()
    
    # Create release configuration
    release_config = await create_release()
    
    # Save configurations to files
    config_dir = project_root / "config" / "github"
    config_dir.mkdir(exist_ok=True)
    
    with open(config_dir / "repository_config.json", "w") as f:
        json.dump(repo_config, f, indent=2)
    
    with open(config_dir / "release_config.json", "w") as f:
        json.dump(release_config, f, indent=2)
    
    print(f"\n✅ Configuration files saved to {config_dir}")
    print("\n🎉 Setup complete! Use the GitHub MCP server in Cursor to:")
    print("1. Create the repository")
    print("2. Push the code")
    print("3. Create the release")

if __name__ == "__main__":
    asyncio.run(main()) 