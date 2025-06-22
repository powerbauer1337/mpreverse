# MarsPro BLE Device Emulation Guide

## Overview
This guide provides multiple approaches to emulate a MarsPro BLE device for reverse engineering and testing purposes.

## Current System: Windows 10
- **Limitation**: Windows 10 does not natively support BLE peripheral (GATT server) mode
- **Available**: BLE client/central mode only
- **Solution**: Use alternative approaches

## Emulation Options

### 1. **nRF Connect on Android Phone (Recommended - Immediate)**
**Best for**: Quick setup, no coding required, immediate results

#### Setup Instructions
1. **Install nRF Connect for Mobile**
   - Download from Google Play Store
   - Free app by Nordic Semiconductor

2. **Create GATT Server Configuration**
   - Open nRF Connect → Menu → GATT Server
   - Create new configuration named "MarsPro Emulator"

3. **Add MarsPro Service**
   - Service UUID: `0000ffe0-0000-1000-8000-00805f9b34fb`

4. **Add Characteristics**
   - **Command**: `0000ffe1-0000-1000-8000-00805f9b34fb` (Write)
   - **Data**: `0000ffe2-0000-1000-8000-00805f9b34fb` (Read, Notify)
   - **Config**: `0000ffe3-0000-1000-8000-00805f9b34fb` (Read, Write)
   - **Status**: `0000ffe4-0000-1000-8000-00805f9b34fb` (Read, Notify)

5. **Configure Advertising**
   - Name: "MarsPro Controller"
   - Enable Scannable and Connectable
   - Add Service UUID to advertising data

6. **Start Advertising**
   - Enable the advertising template
   - Device will appear in BLE scans

#### Advantages
- ✅ Works immediately
- ✅ No coding required
- ✅ Can monitor traffic in real-time
- ✅ Supports all BLE operations

#### Disadvantages
- ❌ Limited programmability
- ❌ Requires Android phone
- ❌ Static responses only

---

### 2. **WSL2 with BlueZ (Recommended - Full Control)**
**Best for**: Full programmability, protocol development, automated testing

#### Prerequisites
- Windows 11 (recommended) or Windows 10 with virtualization enabled
- WSL2 installed with Ubuntu
- Bluetooth adapter accessible to WSL2

#### Setup Steps
1. **Enable WSL2** (Run as Administrator)
   ```powershell
   dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
   dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
   ```

2. **Restart and Install Ubuntu**
   ```powershell
   wsl --set-default-version 2
   wsl --install -d Ubuntu
   ```

3. **Run Setup Script**
   ```bash
   # In WSL2 Ubuntu
   cd /mnt/c/Users/marvi/Coding/MarsPro
   chmod +x scripts/setup_wsl2_ble_emulator.sh
   ./scripts/setup_wsl2_ble_emulator.sh
   ```

4. **Start Emulator**
   ```bash
   cd ~/marspro_ble_emulator
   source ~/marspro_ble_env/bin/activate
   python3 marspro_gatt_server.py
   ```

#### Advantages
- ✅ Full programmability
- ✅ Can implement complex protocol logic
- ✅ Automated testing capabilities
- ✅ Traffic logging and analysis
- ✅ Can respond dynamically to commands

#### Disadvantages
- ❌ Complex setup
- ❌ Requires WSL2 and Linux knowledge
- ❌ Bluetooth adapter access can be tricky

---

### 3. **ESP32 Development Board (Hardware Solution)**
**Best for**: Hardware-level emulation, learning embedded BLE

#### Setup
1. **Hardware Required**
   - ESP32 development board
   - USB cable
   - Arduino IDE or ESP-IDF

2. **Programming**
   - Use Arduino BLE libraries
   - Implement GATT server with MarsPro UUIDs
   - Program command handling logic

#### Advantages
- ✅ Hardware-level emulation
- ✅ Can be deployed as standalone device
- ✅ Good for learning embedded BLE

#### Disadvantages
- ❌ Requires hardware purchase
- ❌ More complex programming
- ❌ Limited debugging capabilities

---

### 4. **Windows BLE Analyzer (Current Implementation)**
**Best for**: Protocol analysis, traffic monitoring, device discovery

#### Current Implementation
- **File**: `scripts/marspro_ble_analyzer.py`
- **Purpose**: Analyze BLE traffic from real MarsPro devices
- **Capability**: BLE client only (cannot emulate device)

#### Usage
```bash
python scripts/marspro_ble_analyzer.py
```

#### Advantages
- ✅ Works on current Windows setup
- ✅ Can discover and analyze real devices
- ✅ Logs all BLE traffic
- ✅ Generates analysis reports

#### Disadvantages
- ❌ Cannot emulate device (client only)
- ❌ Requires real MarsPro device for testing
- ❌ Limited to analysis only

---

## Recommended Approach

### **Phase 1: Immediate Testing (nRF Connect)**
1. Set up nRF Connect on Android phone
2. Configure MarsPro GATT server
3. Test with MarsPro app
4. Document observed protocol patterns

### **Phase 2: Full Development (WSL2)**
1. Set up WSL2 with Ubuntu
2. Install and configure BlueZ
3. Implement programmable BLE emulator
4. Develop complete protocol implementation

### **Phase 3: Integration Testing**
1. Use emulator for Home Assistant integration testing
2. Implement automated test scenarios
3. Validate protocol implementation

---

## Protocol Discovery Strategy

### **Using nRF Connect**
1. **Monitor Traffic**: Watch characteristic reads/writes in real-time
2. **Document Patterns**: Note command structures and responses
3. **Test Commands**: Try different app functions and observe BLE traffic
4. **Export Logs**: Save traffic logs for analysis

### **Using WSL2 Emulator**
1. **Implement Basic Responses**: Start with static responses
2. **Add Command Handling**: Implement logic for each command type
3. **Dynamic Responses**: Make responses based on device state
4. **Protocol Refinement**: Iterate based on app behavior

---

## Troubleshooting

### **nRF Connect Issues**
- **App won't connect**: Check UUIDs match exactly
- **No advertising**: Ensure advertising is enabled
- **Permission issues**: Grant location permissions

### **WSL2 Issues**
- **No Bluetooth adapter**: Check Windows Bluetooth settings
- **Permission denied**: Add user to bluetooth group
- **Service won't start**: Restart bluetooth service

### **Windows BLE Issues**
- **Scanner fails**: Ensure Bluetooth is enabled
- **No devices found**: Check device proximity and power
- **Permission errors**: Run as administrator if needed

---

## Next Steps

1. **Start with nRF Connect** for immediate testing
2. **Set up WSL2** for full development environment
3. **Use Windows analyzer** to study real devices
4. **Implement protocol** based on discovered patterns
5. **Test integration** with Home Assistant

---

## Files Created

- `scripts/marspro_ble_analyzer.py`: Windows BLE traffic analyzer
- `scripts/marspro_ble_emulator_nrf_guide.md`: nRF Connect setup guide
- `scripts/setup_wsl2_ble_emulator.sh`: WSL2 setup script
- `analysis/ble_emulation_guide.md`: This comprehensive guide

---

## Success Criteria

- ✅ MarsPro app can discover and connect to emulator
- ✅ Basic commands (on/off, status) work
- ✅ Protocol patterns are documented
- ✅ Home Assistant integration can be tested
- ✅ Automated testing is possible

---

**Choose your preferred approach and start with the immediate solution (nRF Connect) while setting up the full development environment (WSL2) in parallel.** 