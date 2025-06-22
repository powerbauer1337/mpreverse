# MarsPro Reverse Engineering & Home Assistant Integration

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Home Assistant](https://img.shields.io/badge/Home%20Assistant-2024.1+-orange.svg)](https://www.home-assistant.io/)

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

## 📋 Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [Analysis Results](#analysis-results)
- [Home Assistant Integration](#home-assistant-integration)
- [Configuration](#configuration)
- [Development](#development)
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
   pip install -r requirements.txt
   ```

3. **Install Home Assistant integration**
   ```bash
   # Copy the integration to your Home Assistant config
   cp -r custom_components/marspro /path/to/homeassistant/config/custom_components/
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
├── custom_components/marspro/     # Home Assistant integration
│   ├── __init__.py               # Main integration file
│   ├── api.py                    # API client (cloud + BLE)
│   ├── config_flow.py            # Configuration UI
│   ├── const.py                  # Constants and configuration
│   ├── coordinator.py             # Data coordinator
│   ├── light.py                  # Light platform
│   └── manifest.json             # Integration manifest
├── docs/                         # Documentation
│   ├── analysis.md               # APK analysis results
│   ├── endpoints.md              # API endpoint documentation
│   └── project_summary.md        # Project overview
├── scripts/                      # Analysis and utility scripts
│   ├── analyze.py                # APK analysis script
│   ├── ble_hook.js               # Frida BLE hook
│   └── setup_github_repo.ps1     # GitHub setup script
├── configuration_samples/         # Configuration examples
│   └── marspro_configuration.yaml
├── output/                       # Analysis outputs
│   ├── apktool_output/           # APK decompilation
│   └── jadx_output/              # Java source code
└── tools/                        # Analysis tools
    ├── jadx/                     # JADX decompiler
    └── frida/                    # Frida scripts
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
- **Switch Platform**: Device power switches (planned)

### Configuration Options

```yaml
marspro:
  # Connection settings
  connection_mode: "auto"  # auto, ble, cloud
  username: "your_email@example.com"
  password: "your_password"
  
  # BLE settings
  ble_scan_timeout: 10
  ble_connect_timeout: 30
  
  # Cloud settings
  cloud_api_url: "https://api.marspro.com"
  
  # Device configuration
  devices:
    - name: "Grow Light 1"
      mac_address: "A0:B1:C2:D3:E4:F5"
      device_type: "light"
      room: "Grow Room"
      
    - name: "Grow Light 2"
      mac_address: "A0:B1:C2:D3:E4:F6"
      device_type: "light"
      room: "Grow Room"
```

## ⚙️ Configuration

### Basic Configuration

```yaml
# configuration.yaml
marspro:
  username: your_email@example.com
  password: your_password
```

### Advanced Configuration

```yaml
# configuration.yaml
marspro:
  # Connection settings
  connection_mode: "ble"  # Use BLE for local control
  username: your_email@example.com
  password: your_password
  
  # BLE configuration
  ble_scan_timeout: 15
  ble_connect_timeout: 30
  ble_retry_attempts: 3
  
  # Cloud configuration
  cloud_api_url: "https://api.marspro.com"
  cloud_timeout: 30
  
  # Device discovery
  auto_discover: true
  discovery_timeout: 60
  
  # Logging
  debug: false
```

### Automation Examples

```yaml
# automations.yaml

# Sunrise automation
- alias: "Grow lights sunrise sequence"
  description: "Gradually increase light intensity at sunrise"
  trigger:
    platform: sun
    event: sunrise
  action:
    - service: light.turn_on
      target:
        entity_id: light.grow_light
      data:
        brightness: 64
    - delay: "00:30:00"
    - service: light.turn_on
      target:
        entity_id: light.grow_light
      data:
        brightness: 128
    - delay: "00:30:00"
    - service: light.turn_on
      target:
        entity_id: light.grow_light
      data:
        brightness: 255

# Sunset automation
- alias: "Grow lights sunset sequence"
  description: "Gradually decrease light intensity at sunset"
  trigger:
    platform: sun
    event: sunset
  action:
    - service: light.turn_on
      target:
        entity_id: light.grow_light
      data:
        brightness: 128
    - delay: "00:30:00"
    - service: light.turn_on
      target:
        entity_id: light.grow_light
      data:
        brightness: 64
    - delay: "00:30:00"
    - service: light.turn_off
      target:
        entity_id: light.grow_light

# Timer-based automation
- alias: "Grow light timer"
  description: "Run grow lights for 12 hours"
  trigger:
    platform: time
    at: "08:00:00"
  action:
    - service: light.turn_on
      target:
        entity_id: light.grow_light
      data:
        brightness: 255
    - delay: "12:00:00"
    - service: light.turn_off
      target:
        entity_id: light.grow_light
```

### Script Examples

```yaml
# scripts.yaml

# Morning routine
morning_grow_routine:
  alias: "Morning Grow Routine"
  sequence:
    - service: light.turn_on
      target:
        entity_id: light.grow_light
      data:
        brightness: 128
    - service: notify.mobile_app
      data:
        message: "Grow lights are now on at 50% brightness"

# Evening routine
evening_grow_routine:
  alias: "Evening Grow Routine"
  sequence:
    - service: light.turn_on
      target:
        entity_id: light.grow_light
      data:
        brightness: 64
    - delay: "01:00:00"
    - service: light.turn_off
      target:
        entity_id: light.grow_light
    - service: notify.mobile_app
      data:
        message: "Grow lights are now off"

# Emergency shutdown
emergency_grow_shutdown:
  alias: "Emergency Grow Shutdown"
  sequence:
    - service: light.turn_off
      target:
        entity_id: light.grow_light
    - service: notify.mobile_app
      data:
        message: "Emergency: All grow lights have been shut down"
```

## 🛠️ Development

### Setting Up Development Environment

1. **Clone and setup**
   ```bash
   git clone https://github.com/your-username/marspro-analysis.git
   cd marspro-analysis
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements-dev.txt
   ```

2. **Install pre-commit hooks**
   ```bash
   pre-commit install
   ```

3. **Run tests**
   ```bash
   pytest tests/
   ```

### Analysis Tools

#### Static Analysis

```bash
# Analyze APK
python scripts/analyze.py apks/MarsPro.apk

# Generate documentation
python scripts/generate_docs.py
```

#### Dynamic Analysis

```bash
# Start Frida server
adb push frida-server /data/local/tmp/
adb shell "chmod 755 /data/local/tmp/frida-server"
adb shell "/data/local/tmp/frida-server &"

# Run BLE hooks
frida -U -f com.marspro.app -l scripts/ble_hook.js
```

### Adding New Features

1. **Create feature branch**
   ```bash
   git checkout -b feature/new-feature
   ```

2. **Implement changes**
   - Follow coding guidelines
   - Add tests
   - Update documentation

3. **Submit pull request**
   ```bash
   git push origin feature/new-feature
   ```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### How to Contribute

1. **Fork the repository**
2. **Create a feature branch**
3. **Make your changes**
4. **Add tests**
5. **Submit a pull request**

### Development Guidelines

- Follow PEP 8 Python style guidelines
- Use type hints for all functions
- Write comprehensive tests
- Update documentation for new features
- Follow Home Assistant integration guidelines

### Reporting Issues

- Use the bug report template
- Include device information and logs
- Provide steps to reproduce
- Check existing issues first

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **MarsPro**: For creating innovative smart devices
- **Home Assistant Community**: For the excellent integration framework
- **Frida Project**: For powerful dynamic analysis tools
- **JADX Team**: For excellent APK decompilation tools

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/your-username/marspro-analysis/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-username/marspro-analysis/discussions)
- **Documentation**: [Project Wiki](https://github.com/your-username/marspro-analysis/wiki)

## 🔗 Related Projects

- [Home Assistant](https://www.home-assistant.io/)
- [Frida](https://frida.re/)
- [JADX](https://github.com/skylot/jadx)
- [Flutter Reactive BLE](https://github.com/PhilipsHue/flutter_reactive_ble)

---

**Disclaimer**: This project is for educational and interoperability purposes. Please respect the terms of service of the original applications and use this integration responsibly. 