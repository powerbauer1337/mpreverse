# MarsPro Project Structure

## Overview

This document describes the reorganized structure of the MarsPro reverse engineering project for better workflow and organization.

## Directory Structure

```
MarsPro/
├── 📁 src/                            # Source code and main components
│   ├── 📁 marspro/                    # Home Assistant integration
│   │   ├── __init__.py               # Main component initialization
│   │   ├── api.py                    # API client for MarsPro devices
│   │   ├── config_flow.py            # Configuration UI
│   │   ├── const.py                  # Constants and configuration
│   │   ├── coordinator.py            # Data coordinator
│   │   ├── light.py                  # Light platform
│   │   └── manifest.json             # Component metadata
│   └── 📁 review_gate/               # Review Gate V2 integration
│       ├── __init__.py               # Review Gate initialization
│       ├── mcp_server.py             # MCP server implementation
│       └── config.py                 # Review Gate configuration
│
├── 📁 analysis/                       # Analysis documentation and logs
│   ├── analysis.log                   # Analysis execution logs
│   ├── analysis_summary.md            # Analysis progress summary
│   ├── api_documentation.md           # API endpoint documentation
│   ├── api_mapping.md                 # Cloud vs local function mapping
│   └── protocols/                     # Discovered protocols
│       ├── ble_protocol.md           # BLE communication protocol
│       └── cloud_api.md              # Cloud API documentation
│
├── 📁 assets/                         # Static assets and binaries
│   ├── 📁 apks/                      # APK files for analysis
│   │   └── MarsPro_1.3.2_APKPure.xapk # Target APK file
│   ├── 📁 tools/                     # External tool binaries
│   │   ├── jadx/                     # JADX decompiler
│   │   └── apktool/                  # APKTool
│   └── 📁 review_gate/               # Review Gate assets
│       ├── cursor-extension/         # Cursor IDE extension
│       └── installers/               # Installation scripts
│
├── 📁 config/                         # Configuration files
│   ├── mcp.json                      # MCP server configuration
│   ├── home_assistant/               # Home Assistant configs
│   │   └── marspro_configuration.yaml # Complete configuration example
│   └── development/                  # Development configs
│       ├── .pre-commit-config.yaml   # Pre-commit hooks
│       └── pytest.ini               # Test configuration
│
├── 📁 docs/                           # Project documentation
│   ├── README.md                     # Main project documentation
│   ├── CONTRIBUTING.md               # Contribution guidelines
│   ├── INSTALLATION.md               # Installation guide
│   ├── API.md                        # API documentation
│   └── DEVELOPMENT.md                # Development guide
│
├── 📁 scripts/                        # Analysis and automation scripts
│   ├── analyze.py                    # Main analysis orchestrator
│   ├── setup.py                      # Project setup script
│   ├── frida/                        # Frida analysis scripts
│   │   ├── net_hook.js               # HTTP interception
│   │   └── ble_hook.js               # BLE interception
│   └── utilities/                    # Utility scripts
│       ├── setup_github_repo.ps1     # GitHub setup script
│       └── test_mcp_servers.py       # MCP server testing
│
├── 📁 tools/                          # Analysis tools and MCP servers
│   ├── 📁 mcp_servers/               # MCP server implementations
│   │   ├── apktool_server/           # APKTool MCP server
│   │   ├── jadx_server/              # JADX MCP server
│   │   └── reverse_engineering/      # Reverse engineering assistant
│   └── 📁 external/                  # External tools
│       └── reverse-engineering-assistant-main/
│
├── 📁 tests/                          # Test suite
│   ├── 📁 unit/                      # Unit tests
│   │   ├── test_api.py               # API tests
│   │   └── test_coordinator.py       # Coordinator tests
│   ├── 📁 integration/               # Integration tests
│   │   └── test_home_assistant.py    # Home Assistant integration tests
│   └── 📁 fixtures/                  # Test fixtures and data
│
├── 📁 output/                         # Analysis output files
│   ├── apktool_output/               # apktool decompilation output
│   ├── jadx_output/                  # jadx decompilation output
│   └── logs/                         # Analysis logs
│
├── 📄 setup.py                        # Package installation script
├── 📄 requirements.txt                # Production dependencies
├── 📄 requirements-dev.txt            # Development dependencies
├── 📄 pyproject.toml                  # Modern Python project configuration
├── 📄 .gitignore                      # Git ignore patterns
├── 📄 LICENSE                         # Project license
└── 📄 README.md                       # Project overview
```

## File Descriptions

### Core Source Code

#### `src/marspro/`
- **Purpose**: Home Assistant integration component
- **Components**:
  - `__init__.py`: Component initialization and configuration
  - `api.py`: API client for MarsPro devices (BLE + Cloud)
  - `config_flow.py`: Configuration UI for Home Assistant
  - `const.py`: Constants and configuration keys
  - `coordinator.py`: Data coordinator for device management
  - `light.py`: Light platform implementation
  - `manifest.json`: Component metadata and dependencies

#### `src/review_gate/`
- **Purpose**: Review Gate V2 MCP server integration
- **Components**:
  - `__init__.py`: Review Gate initialization
  - `mcp_server.py`: MCP server implementation
  - `config.py`: Review Gate configuration

### Analysis Tools

#### `tools/mcp_servers/`
- **Purpose**: MCP server implementations for analysis tools
- **Servers**:
  - `apktool_server/`: APKTool MCP server
  - `jadx_server/`: JADX MCP server
  - `reverse_engineering/`: Reverse engineering assistant

#### `scripts/frida/`
- **Purpose**: Frida analysis scripts for dynamic analysis
- **Scripts**:
  - `net_hook.js`: HTTP/HTTPS traffic interception
  - `ble_hook.js`: BLE communication interception

### Configuration

#### `config/`
- **Purpose**: All configuration files
- **Files**:
  - `mcp.json`: MCP server configuration
  - `home_assistant/`: Home Assistant configuration examples
  - `development/`: Development tool configurations

### Documentation

#### `docs/`
- **Purpose**: Comprehensive project documentation
- **Files**:
  - `README.md`: Main project documentation
  - `CONTRIBUTING.md`: Contribution guidelines
  - `INSTALLATION.md`: Installation guide
  - `API.md`: API documentation
  - `DEVELOPMENT.md`: Development guide

### Assets

#### `assets/`
- **Purpose**: Static assets and binaries
- **Directories**:
  - `apks/`: APK files for analysis
  - `tools/`: External tool binaries
  - `review_gate/`: Review Gate assets and extensions

## Analysis Workflow

### Phase 1: Static Analysis
1. **Input**: APK file in `assets/apks/` directory
2. **Tools**: APKTool and JADX MCP servers in `tools/mcp_servers/`
3. **Output**: Decompiled files in `output/` directory
4. **Documentation**: Extracted files in `analysis/` directory

### Phase 2: Dynamic Analysis
1. **Input**: Decompiled APK and Frida scripts
2. **Tools**: Frida scripts in `scripts/frida/`
3. **Scripts**: `net_hook.js`, `ble_hook.js`
4. **Output**: Network and BLE traffic logs in `output/logs/`

### Phase 3: Documentation
1. **Input**: Analysis results
2. **Output**: Updated documentation in `docs/` and `analysis/`
3. **Files**: API documentation, protocol mapping, analysis summary

### Phase 4: Home Assistant Integration
1. **Input**: Discovered APIs and protocols
2. **Output**: Updated Home Assistant component in `src/marspro/`
3. **Configuration**: Examples in `config/home_assistant/`

### Phase 5: Testing
1. **Input**: Complete integration
2. **Output**: Test results and validation
3. **Tests**: Unit and integration tests in `tests/`

## Key Improvements

### 1. Clear Separation of Concerns
- **Source Code**: All source code in `src/` directory
- **Tools**: Analysis tools in `tools/` directory
- **Assets**: Static files in `assets/` directory
- **Configuration**: All configs in `config/` directory

### 2. Better Organization
- **MCP Servers**: Dedicated directory for MCP server implementations
- **Review Gate**: Integrated into source code structure
- **Tests**: Comprehensive test suite with proper organization
- **Documentation**: Centralized and well-structured

### 3. Modern Python Project Structure
- **pyproject.toml**: Modern Python project configuration
- **setup.py**: Proper package installation
- **Requirements**: Separated production and development dependencies

### 4. Asset Management
- **APKs**: Organized in assets directory
- **Tools**: External binaries properly managed
- **Extensions**: Review Gate assets organized

## Usage Instructions

### Initial Setup
1. Install dependencies: `pip install -r requirements.txt`
2. Install development dependencies: `pip install -r requirements-dev.txt`
3. Configure MCP servers in `config/mcp.json`
4. Place APK file in `assets/apks/` directory

### Running Analysis
1. **Full Analysis**: `python scripts/analyze.py assets/apks/MarsPro_1.3.2_APKPure.xapk`
2. **Individual Phases**: Modify `scripts/analyze.py` to run specific phases
3. **Manual Frida**: Use individual Frida scripts for dynamic analysis

### Home Assistant Integration
1. Copy `src/marspro/` to Home Assistant config directory
2. Use `config/home_assistant/marspro_configuration.yaml` as template
3. Update configuration with discovered device information

### Development
1. **Running Tests**: `pytest tests/`
2. **Code Formatting**: `black src/ tests/`
3. **Linting**: `flake8 src/ tests/`
4. **Pre-commit**: `pre-commit run --all-files`

## Notes

- All analysis output is organized in dedicated directories
- Documentation is automatically generated during analysis
- Home Assistant integration is ready for discovered APIs
- MCP tools provide enhanced analysis capabilities
- Project structure supports collaborative development
- Modern Python packaging standards are followed
- Clear separation between source code, tools, and assets

---

*Last Updated: 2025-01-22* 