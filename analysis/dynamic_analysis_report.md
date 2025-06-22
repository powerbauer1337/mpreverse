# MarsPro Dynamic Analysis Report

## Analysis Summary

This report contains findings from dynamic analysis of the MarsPro application using Frida hooks.

## Prerequisites

### Required Tools
- Frida (Python package)
- ADB (Android Debug Bridge)
- Rooted Android device (for Frida server)

### Setup Instructions
1. Install Frida: `pip install frida-tools`
2. Install Frida server on rooted device
3. Enable USB debugging on Android device
4. Connect device via USB

## Hook Scripts

### BLE Hook Script
- **File**: `scripts/frida/enhanced_ble_hook.js`
- **Purpose**: Capture Bluetooth Low Energy communication
- **Hooks**:
  - BluetoothGatt operations
  - BluetoothGattCallback events
  - Service discovery

### Network Hook Script
- **File**: `scripts/frida/enhanced_network_hook.js`
- **Purpose**: Capture network API calls
- **Hooks**:
  - OkHttp requests
  - HTTP communication

## Usage Instructions

1. **Start the analysis**:
   ```bash
   python scripts/dynamic_analysis.py
   ```

2. **Run Frida manually**:
   ```bash
   frida -U -f com.marspro.meizhi -l scripts/frida/enhanced_ble_hook.js -l scripts/frida/enhanced_network_hook.js
   ```

3. **Use the MarsPro app**:
   - Launch the app
   - Connect to a MarsPro device
   - Perform various operations
   - Monitor the console output

## Expected Findings

### BLE Communication
- Device discovery process
- Service discovery
- Characteristic reads/writes
- Notification subscriptions

### Network Communication
- Firebase authentication
- API endpoints
- Data synchronization
- Cloud storage operations

## Next Steps

1. **Document discovered protocols**
2. **Implement communication libraries**
3. **Create Home Assistant integration**
4. **Test with actual devices**

---

**Generated**: 2025-06-22 20:18:04
**Version**: 1.0
