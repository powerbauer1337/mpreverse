# MarsPro Reverse Engineering Analysis Report

## Executive Summary

This report details the reverse engineering analysis of the MarsPro Android application (version 1.3.2), a Flutter-based plant growing/hydroponics control system. The analysis reveals a sophisticated IoT application that controls various environmental parameters for plant cultivation.

## Application Overview

### Basic Information
- **Package Name**: `com.marspro.meizhi`
- **Version**: 1.3.2
- **Platform**: Flutter (Android)
- **Architecture**: ARM64 (primary target)
- **Firebase Project**: `mars-pro-930a4`

### Application Type
MarsPro is a **plant growing/hydroponics control application** that manages environmental parameters for optimal plant growth.

## Key Features Identified

### Environmental Control Systems
Based on asset analysis, the app controls:

1. **Lighting Systems**:
   - UV lights
   - PPFD (Photosynthetic Photon Flux Density) control
   - Vegetative light control
   - General lighting

2. **Climate Control**:
   - Temperature monitoring and control
   - Humidity control (humidifier/dehumidifier)
   - CO2 monitoring
   - VPD (Vapor Pressure Deficit) monitoring

3. **Air Management**:
   - Fan control
   - Wind speed monitoring
   - Air volume control
   - Wind pressure monitoring

4. **Water Management**:
   - Drip system control
   - Water flow monitoring

5. **Additional Features**:
   - Timer functionality
   - Scene management
   - Auto mode
   - Manual control modes

## Technical Architecture

### Communication Protocols
The app uses multiple communication methods:

1. **Bluetooth Low Energy (BLE)**:
   - Primary local communication protocol
   - Direct device control
   - Real-time sensor data

2. **WiFi/Internet**:
   - Cloud connectivity
   - Remote monitoring
   - Data synchronization

3. **Firebase Integration**:
   - Authentication
   - Cloud storage
   - Analytics
   - Crash reporting

### Permissions Analysis
```xml
<!-- Network & Internet -->
<uses-permission android:name="android.permission.INTERNET"/>
<uses-permission android:name="android.permission.ACCESS_NETWORK_STATE"/>
<uses-permission android:name="android.permission.ACCESS_WIFI_STATE"/>
<uses-permission android:name="android.permission.CHANGE_WIFI_STATE"/>

<!-- Bluetooth -->
<uses-permission android:name="android.permission.BLUETOOTH"/>
<uses-permission android:name="android.permission.BLUETOOTH_SCAN"/>
<uses-permission android:name="android.permission.BLUETOOTH_ADVERTISE"/>
<uses-permission android:name="android.permission.BLUETOOTH_CONNECT"/>
<uses-permission android:name="android.permission.BLUETOOTH_ADMIN"/>

<!-- Location (required for BLE scanning) -->
<uses-permission android:name="android.permission.ACCESS_FINE_LOCATION"/>
<uses-permission android:name="android.permission.ACCESS_COARSE_LOCATION"/>

<!-- Storage & Media -->
<uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE"/>
<uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE"/>
<uses-permission android:name="android.permission.READ_MEDIA_IMAGES"/>
<uses-permission android:name="android.permission.READ_MEDIA_AUDIO"/>
<uses-permission android:name="android.permission.READ_MEDIA_VIDEO"/>

<!-- Camera -->
<uses-permission android:name="android.permission.CAMERA"/>

<!-- Notifications -->
<uses-permission android:name="android.permission.POST_NOTIFICATIONS"/>
<uses-permission android:name="android.permission.VIBRATE"/>
<uses-permission android:name="android.permission.RECEIVE_BOOT_COMPLETED"/>
```

## Code Analysis

### Obfuscation Level
- **High obfuscation**: All class names and methods are obfuscated
- **String encryption**: Likely present based on obfuscation patterns
- **Native code**: Possible native libraries for BLE communication

### Flutter Structure
The app is built with Flutter and includes:
- Custom assets for UI elements
- Multiple language support
- Responsive design elements
- Platform-specific integrations

## Security Analysis

### Code Protection
- Heavy obfuscation makes static analysis challenging
- Likely uses code obfuscation tools (ProGuard/R8)
- Native code components for sensitive operations

### Network Security
- Uses HTTPS for cloud communication
- Firebase security rules likely in place
- BLE communication may be encrypted

## Reverse Engineering Challenges

### Static Analysis Limitations
1. **Obfuscated Code**: All meaningful identifiers are obfuscated
2. **Native Libraries**: BLE communication likely in native code
3. **String Encryption**: Important strings may be encrypted
4. **Anti-Debugging**: Possible anti-debugging measures

### Dynamic Analysis Opportunities
1. **Frida Hooks**: Can intercept BLE communication
2. **Network Monitoring**: Can capture API calls
3. **Runtime Analysis**: Can observe actual behavior

## Home Assistant Integration Strategy

### Communication Protocol Reverse Engineering
1. **BLE Protocol Analysis**:
   - Use Frida to hook BLE operations
   - Monitor characteristic reads/writes
   - Identify service UUIDs and characteristic UUIDs

2. **API Endpoint Discovery**:
   - Monitor network traffic
   - Identify Firebase endpoints
   - Understand data formats

3. **Authentication Flow**:
   - Analyze login process
   - Understand token management
   - Identify device pairing process

### Implementation Plan
1. **Phase 1**: BLE Communication Protocol
   - Reverse engineer BLE service structure
   - Document characteristic mappings
   - Implement basic communication

2. **Phase 2**: Device Control
   - Implement device discovery
   - Add device control commands
   - Handle sensor data parsing

3. **Phase 3**: Home Assistant Integration
   - Create custom component
   - Implement device entities
   - Add configuration flow

## Next Steps

### Immediate Actions
1. **Dynamic Analysis Setup**:
   - Install Frida on test device
   - Set up network monitoring
   - Prepare BLE analysis tools

2. **Protocol Discovery**:
   - Hook BLE operations
   - Monitor network traffic
   - Document API endpoints

3. **Device Testing**:
   - Obtain MarsPro device for testing
   - Document device behavior
   - Test communication protocols

### Long-term Goals
1. **Complete Protocol Documentation**
2. **Home Assistant Component Development**
3. **Community Integration**
4. **Documentation and Tutorials**

## Conclusion

The MarsPro application is a sophisticated IoT control system with strong security measures. While static analysis is limited due to heavy obfuscation, dynamic analysis using Frida and network monitoring should reveal the communication protocols needed for Home Assistant integration.

The app's focus on plant growing automation makes it an excellent candidate for smart home integration, allowing users to control their hydroponics systems through Home Assistant without cloud dependency.

---

**Analysis Date**: June 22, 2025  
**Analyst**: AI Assistant  
**Version**: 1.0 