# MarsPro Reverse Engineering & Home Assistant Integration

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Home Assistant](https://img.shields.io/badge/Home%20Assistant-2024.1+-orange.svg)](https://www.home-assistant.io/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A comprehensive reverse engineering project for MarsPro smart devices, enabling local control through Home Assistant without cloud dependency.

## 🎯 Project Overview

This project reverse engineers the MarsPro Android application to understand the communication protocols used by MarsPro smart devices. The goal is to create a local Home Assistant integration that allows full control of MarsPro devices without requiring cloud services.

### Key Features

- 🔍 **Complete APK Analysis**: Static and dynamic analysis of the MarsPro Android app
- 🏠 **Home Assistant Integration**: Local control of MarsPro devices
- 📡 **BLE Communication**: Direct Bluetooth Low Energy communication
- ☁️ **Cloud API Support**: Fallback to cloud API when needed
- 📚 **Comprehensive Documentation**: Detailed analysis and implementation guides
- 🛠️ **Analysis Tools**: Frida scripts and utilities for protocol discovery
- 🧪 **Test Suite**: Comprehensive unit and integration tests
- 🔧 **Modern Development**: Modern Python packaging and development tools

## 📋 Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [Analysis Results](#analysis-results)
- [Home Assistant Integration](#home-assistant-integration)
- [Configuration](#configuration)
- [Development](#development)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- Home Assistant 2024.1 or higher
- Git
- Android device with MarsPro app (for dynamic analysis)

### Quick Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/marspro-analysis.git
   cd marspro-analysis
   ```

2. **Install dependencies**
   ```bash
   # Install production dependencies
   pip install -r requirements.txt
   
   # Install development dependencies
   pip install -r requirements-dev.txt
   ```

3. **Install Home Assistant integration**
   ```bash
   # Copy the integration to your Home Assistant config
   cp -r src/marspro /path/to/homeassistant/config/custom_components/
   ```

## ⚡ Quick Start

### 1. Basic Setup

1. **Add the integration to Home Assistant**
   - Go to Settings → Devices & Services
   - Click "Add Integration"
   - Search for "MarsPro"
   - Enter your device credentials

2. **Configure your devices**
   ```yaml
   # configuration.yaml
   marspro:
     username: your_email@example.com
     password: your_password
     devices:
       - name: "Living Room Light"
         mac_address: "A0:B1:C2:D3:E4:F5"
         device_type: "light"
   ```

3. **Restart Home Assistant**

### 2. Using BLE Mode (Recommended)

For local control without cloud dependency:

```yaml
# configuration.yaml
marspro:
  connection_mode: "ble"
  devices:
    - name: "Grow Light"
      mac_address: "A0:B1:C2:D3:E4:F5"
      device_type: "light"
      ble_scan_timeout: 10
```

### 3. Automation Examples

```yaml
# automations.yaml
- alias: "Turn on grow lights at sunrise"
  trigger:
    platform: sun
    event: sunrise
  action:
    - service: light.turn_on
      target:
        entity_id: light.grow_light
      data:
        brightness: 255

- alias: "Turn off lights at sunset"
  trigger:
    platform: sun
    event: sunset
  action:
    - service: light.turn_off
      target:
        entity_id: light.grow_light
```

## 📁 Project Structure

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

## 🔍 Analysis Results

### APK Analysis Summary

- **App Type**: Flutter-based Android application
- **BLE Library**: `flutter_reactive_ble`
- **Authentication**: Firebase Authentication
- **Analytics**: Firebase Analytics
- **Key Permissions**: BLUETOOTH, BLUETOOTH_ADMIN, INTERNET, ACCESS_FINE_LOCATION

### Discovered Protocols

1. **BLE Communication**
   - Service UUID: `0000ffe0-0000-1000-8000-00805f9b34fb`
   - Characteristic UUID: `0000ffe1-0000-1000-8000-00805f9b34fb`
   - Protocol: Custom binary protocol

2. **Cloud API**
   - Base URL: `https://api.marspro.com`
   - Authentication: Bearer token
   - Endpoints: Device control, status, user management

### Key Findings

- Devices use both BLE and cloud communication
- BLE provides local control capabilities
- Cloud API offers remote access and device management
- Authentication tokens are stored locally
- Device discovery happens via BLE scanning

## 🏠 Home Assistant Integration

### Supported Features

- ✅ **Light Control**: On/off, brightness adjustment
- ✅ **Device Discovery**: Automatic BLE device discovery
- ✅ **Local Control**: BLE communication for offline operation
- ✅ **Cloud Fallback**: Cloud API when BLE unavailable
- ✅ **Configuration UI**: User-friendly setup interface
- ✅ **Status Updates**: Real-time device status

### Platform Support

- **Light Platform**: Full light entity support
- **Sensor Platform**: Device status sensors (planned)

## 🧪 Testing

### Running Tests

```bash
# Run all tests
pytest

# Run unit tests only
pytest tests/unit/

# Run integration tests only
pytest tests/integration/

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test markers
pytest -m "unit"
pytest -m "integration"
pytest -m "api"
```

### Test Categories

- **Unit Tests**: Individual component testing
- **Integration Tests**: Home Assistant integration testing
- **API Tests**: API client functionality testing
- **BLE Tests**: Bluetooth communication testing

## 🔧 Development

### Code Quality

```bash
# Format code
black src/ tests/

# Lint code
flake8 src/ tests/

# Type checking
mypy src/

# Run pre-commit hooks
pre-commit run --all-files
```

### Development Setup

1. **Install development dependencies**
   ```bash
   pip install -r requirements-dev.txt
   ```

2. **Setup pre-commit hooks**
   ```bash
   pre-commit install
   ```

3. **Configure MCP servers**
   ```bash
   # Copy MCP configuration
   cp config/mcp.json ~/.cursor/mcp.json
   ```

### Analysis Workflow

1. **Static Analysis**
   ```bash
   python scripts/analyze.py assets/apks/MarsPro_1.3.2_APKPure.xapk
   ```

2. **Dynamic Analysis**
   ```bash
   # HTTP interception
   frida -U -f com.marspro.app -l scripts/frida/net_hook.js --no-pause
   
   # BLE interception
   frida -U -f com.marspro.app -l scripts/frida/ble_hook.js --no-pause
   ```

3. **Documentation Generation**
   ```bash
   # Analysis results are automatically documented
   # Check analysis/ directory for generated documentation
   ```

## 📚 Documentation

- **[CONTRIBUTING.md](CONTRIBUTING.md)**: Contribution guidelines
- **[INSTALLATION.md](docs/INSTALLATION.md)**: Detailed installation guide
- **[API.md](docs/API.md)**: API documentation
- **[DEVELOPMENT.md](docs/DEVELOPMENT.md)**: Development guide
- **[PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)**: Project structure documentation

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Process

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

### Code Standards

- Follow PEP 8 style guidelines
- Use type hints for all functions
- Write comprehensive docstrings
- Add tests for new functionality
- Update documentation as needed

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- MarsPro team for creating the original app
- Home Assistant community for integration patterns
- Frida team for dynamic analysis tools
- JADX team for APK decompilation tools

---

**Note**: This project is for educational and research purposes. Please respect the terms of service of the original MarsPro application and use this integration responsibly. 