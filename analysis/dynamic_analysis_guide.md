# MarsPro Dynamic Analysis Guide

## Prerequisites

### Required Hardware
1. **Rooted Android Device**
   - Android 7.0 or higher recommended
   - Root access required for Frida server
   - USB debugging enabled

2. **Physical MarsPro Device**
   - Any MarsPro hydroponics controller
   - Powered on and in range
   - Bluetooth enabled

3. **Computer**
   - Windows/Linux/macOS
   - USB cable for device connection
   - Internet connection for tool downloads

### Required Software
1. **Android SDK Platform Tools (ADB)**
   - Installed via setup script
   - Added to system PATH

2. **Frida**
   - Python package: `pip install frida-tools`
   - Frida server for Android (requires root)

3. **Network Monitoring Tools**
   - Wireshark or similar
   - Burp Suite (optional)

## Setup Instructions

### Step 1: Install Android Tools
```bash
python scripts/utilities/setup_android_tools.py
```

### Step 2: Setup PATH
```bash
# PowerShell
.\scripts\utilities\setup_android_path.ps1

# Batch
.\scripts\utilities\setup_android_path.bat
```

### Step 3: Install Frida Server on Android Device
1. Download Frida server for your Android architecture
2. Push to device: `adb push frida-server /data/local/tmp/`
3. Make executable: `adb shell chmod 755 /data/local/tmp/frida-server`
4. Start server: `adb shell su -c '/data/local/tmp/frida-server &'`

### Step 4: Verify Setup
```bash
# Check ADB
adb devices

# Check Frida
frida --version

# Check device connection
adb shell ps | grep frida
```

## Dynamic Analysis Workflow

### Phase 1: Device Discovery
1. **Scan for BLE devices**
   ```bash
   frida -U -f com.marspro.meizhi -l scripts/frida/enhanced_ble_hook.js
   ```

2. **Monitor device discovery**
   - Look for BLE scanning operations
   - Note device addresses and names
   - Document advertising data

### Phase 2: Connection Analysis
1. **Connect to MarsPro device**
   - Use the MarsPro app to connect
   - Monitor connection establishment
   - Document service discovery

2. **Service enumeration**
   - Capture all service UUIDs
   - Document characteristic UUIDs
   - Note property flags (read/write/notify)

### Phase 3: Protocol Analysis
1. **Command sending**
   - Use app to control devices
   - Monitor characteristic writes
   - Document command formats

2. **Data reading**
   - Monitor characteristic reads
   - Capture sensor data formats
   - Document notification patterns

### Phase 4: Network Analysis
1. **API endpoint discovery**
   - Monitor HTTP requests
   - Document Firebase endpoints
   - Capture authentication flows

2. **Data synchronization**
   - Monitor cloud sync operations
   - Document data formats
   - Understand update mechanisms

## Expected Findings

### BLE Communication
- **Service UUIDs**: Main control service
- **Characteristic UUIDs**: Commands, data, configuration
- **Data Formats**: Binary command structures
- **Security**: Authentication mechanisms

### Network Communication
- **Firebase Endpoints**: Authentication, data sync
- **API Formats**: JSON request/response structures
- **Authentication**: Token-based or certificate-based
- **Data Flow**: Real-time vs batch synchronization

## Documentation

### Required Outputs
1. **BLE Protocol Specification**
   - Service and characteristic UUIDs
   - Command formats and structures
   - Data formats and parsing
   - Error handling

2. **API Documentation**
   - Endpoint URLs and methods
   - Request/response formats
   - Authentication mechanisms
   - Rate limiting

3. **Implementation Guide**
   - Python BLE client example
   - Home Assistant integration
   - Error handling patterns
   - Testing procedures

## Troubleshooting

### Common Issues
1. **Device not detected**
   - Check Bluetooth permissions
   - Verify device is advertising
   - Check Frida server is running

2. **Connection failures**
   - Verify device is in range
   - Check authentication requirements
   - Monitor error messages

3. **No data captured**
   - Verify hooks are installed
   - Check characteristic properties
   - Monitor notification subscriptions

### Debug Commands
```bash
# Check device status
adb shell dumpsys bluetooth

# Monitor BLE logs
adb logcat | grep -i bluetooth

# Check Frida server
adb shell ps | grep frida

# Monitor network
adb shell tcpdump -i any -w /sdcard/capture.pcap
```

## Next Steps

### After Dynamic Analysis
1. **Implement BLE Client**
   - Create Python library
   - Support device discovery
   - Implement command sending

2. **Develop Home Assistant Integration**
   - Create custom component
   - Implement device entities
   - Add configuration flow

3. **Testing and Validation**
   - Test with real devices
   - Validate all features
   - Performance testing

---

**Version**: 1.0  
**Last Updated**: [Date]  
**Status**: Ready for Implementation
