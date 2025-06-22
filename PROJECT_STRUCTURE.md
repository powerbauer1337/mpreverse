# MarsPro Project Structure

## Overview

This document describes the reorganized structure of the MarsPro reverse engineering project for better workflow and organization.

## Directory Structure

```
MarsPro/
├── 📁 apks/                           # APK files for analysis
│   └── MarsPro_1.3.2_APKPure.xapk    # Target APK file
│
├── 📁 analysis/                       # Analysis documentation and logs
│   ├── analysis.log                   # Analysis execution logs
│   ├── analysis_summary.md            # Analysis progress summary
│   ├── api_documentation.md           # API endpoint documentation
│   └── api_mapping.md                 # Cloud vs local function mapping
│
├── 📁 configuration_samples/          # Home Assistant configuration examples
│   └── marspro_configuration.yaml     # Complete configuration example
│
├── 📁 custom_components/              # Home Assistant integration
│   └── 📁 marspro/
│       ├── __init__.py                # Main component initialization
│       ├── const.py                   # Constants and configuration keys
│       ├── manifest.json              # Component metadata
│       └── api.py                     # API client for MarsPro devices
│
├── 📁 docs/                           # Project documentation
│   ├── analysis.md                    # Main analysis documentation
│   └── endpoints.md                   # API endpoints documentation
│
├── 📁 output/                         # Analysis output files
│   ├── apktool_output/                # apktool decompilation output
│   └── jadx_output/                   # jadx decompilation output
│
├── 📁 scripts/                        # Analysis and automation scripts
│   ├── analyze.py                     # Main analysis orchestrator
│   ├── net_hook.js                    # Frida script for HTTP interception
│   └── ble_hook.js                    # Frida script for BLE interception
│
├── 📁 tools/                          # External tools and utilities
│   └── 📁 reverse-engineering-assistant-main/  # MCP server tools
│       ├── src/                       # Source code
│       ├── ghidra_scripts/            # Ghidra analysis scripts
│       ├── lib/                       # Library files
│       └── README.md                  # Tool documentation
│
├── 📁 .cursor/                        # Cursor IDE configuration
│   └── mcp.json                       # MCP server configuration
│
├── 📄 README.md                       # Project overview and setup guide
├── 📄 PROJECT_STRUCTURE.md            # This file
├── 📄 requirements.txt                # Python dependencies
├── 📄 setup.py                        # Installation script
├── 📄 mcp.json                        # Root MCP configuration
└── 📄 task.prompt                     # Original project requirements
```

## File Descriptions

### Core Analysis Files

#### `scripts/analyze.py`
- **Purpose**: Main analysis orchestrator
- **Function**: Runs all 5 phases of the reverse engineering workflow
- **Usage**: `python scripts/analyze.py apks/MarsPro_1.3.2_APKPure.xapk`

#### `scripts/net_hook.js`
- **Purpose**: HTTP/HTTPS traffic interception
- **Function**: Hooks network calls to discover REST API endpoints
- **Usage**: `frida -U -f com.marspro.app -l scripts/net_hook.js --no-pause`

#### `scripts/ble_hook.js`
- **Purpose**: BLE communication interception
- **Function**: Hooks Bluetooth calls to discover BLE protocols
- **Usage**: `frida -U -f com.marspro.app -l scripts/ble_hook.js --no-pause`

### Documentation Files

#### `docs/analysis.md`
- **Purpose**: Main analysis documentation
- **Content**: Analysis phases, workflow, tools, and progress tracking

#### `docs/endpoints.md`
- **Purpose**: API endpoints documentation
- **Content**: REST API endpoints, BLE protocols, and communication formats

#### `analysis/analysis_summary.md`
- **Purpose**: Analysis progress summary
- **Content**: Current status, discovered components, and next steps

### Home Assistant Integration

#### `custom_components/marspro/`
- **Purpose**: Home Assistant custom component
- **Components**:
  - `__init__.py`: Component initialization and configuration
  - `const.py`: Constants and configuration keys
  - `manifest.json`: Component metadata and dependencies
  - `api.py`: API client for MarsPro devices

#### `configuration_samples/marspro_configuration.yaml`
- **Purpose**: Home Assistant configuration examples
- **Content**: Complete configuration with automations and scripts

### Configuration Files

#### `.cursor/mcp.json`
- **Purpose**: MCP server configuration for Cursor IDE
- **Content**: Reverse engineering assistant and other MCP servers

#### `requirements.txt`
- **Purpose**: Python dependencies
- **Dependencies**: frida-tools, uv, mcp, aiohttp, bleak

#### `setup.py`
- **Purpose**: Installation script
- **Function**: Package installation and entry points

## Analysis Workflow

### Phase 1: Static Analysis
1. **Input**: APK file in `apks/` directory
2. **Tools**: apktool, jadx
3. **Output**: Decompiled files in `output/` directory
4. **Documentation**: Extracted files in `analysis/` directory

### Phase 2: Dynamic Analysis
1. **Input**: Decompiled APK and Frida scripts
2. **Tools**: Frida, ADB
3. **Scripts**: `scripts/net_hook.js`, `scripts/ble_hook.js`
4. **Output**: Network and BLE traffic logs

### Phase 3: Documentation
1. **Input**: Analysis results
2. **Output**: Updated documentation in `docs/` and `analysis/`
3. **Files**: API documentation, protocol mapping, analysis summary

### Phase 4: Home Assistant Integration
1. **Input**: Discovered APIs and protocols
2. **Output**: Updated Home Assistant component
3. **Files**: `custom_components/marspro/`, configuration examples

### Phase 5: Testing
1. **Input**: Complete integration
2. **Output**: Test results and validation
3. **Validation**: Unit tests, integration tests, real device testing

## Key Directories

### `apks/`
- Contains target APK files for analysis
- Organized by version and source

### `analysis/`
- Contains analysis documentation and logs
- Generated during the analysis process

### `output/`
- Contains decompiled APK files
- Generated by apktool and jadx

### `scripts/`
- Contains analysis and automation scripts
- Orchestrates the reverse engineering workflow

### `tools/`
- Contains external tools and utilities
- Includes MCP servers and analysis tools

## Usage Instructions

### Initial Setup
1. Install dependencies: `pip install -r requirements.txt`
2. Configure MCP servers in `.cursor/mcp.json`
3. Place APK file in `apks/` directory

### Running Analysis
1. **Full Analysis**: `python scripts/analyze.py apks/MarsPro_1.3.2_APKPure.xapk`
2. **Individual Phases**: Modify `scripts/analyze.py` to run specific phases
3. **Manual Frida**: Use individual Frida scripts for dynamic analysis

### Home Assistant Integration
1. Copy `custom_components/marspro/` to Home Assistant config directory
2. Use `configuration_samples/marspro_configuration.yaml` as template
3. Update configuration with discovered device information

## Notes

- All analysis output is organized in dedicated directories
- Documentation is automatically generated during analysis
- Home Assistant integration is ready for discovered APIs
- MCP tools provide enhanced analysis capabilities
- Project structure supports collaborative development

---

*Last Updated: 2025-06-22*
*Project Status: Phase 1 Complete, Ready for Dynamic Analysis* 