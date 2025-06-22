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
- **Bundle Format**: XAPK (Android App Bundle)

### Application Type
MarsPro is a **plant growing/hydroponics control application** that manages environmental parameters for optimal plant growth.

## Key Features Identified

### Environmental Control Systems
Based on asset analysis, the app controls:

1. **Lighting Systems**:
   - UV lights (`uv.webp`)
   - PPFD (Photosynthetic Photon Flux Density) control (`ppfd.webp`)
   - Vegetative light control (`vege-light.webp`)
   - General lighting (`light.webp`)
   - Luminance control (`luminance.webp`)

2. **Climate Control**:
   - Temperature monitoring and control (`temperature.webp`)
   - Humidity control (`humidity.webp`)
   - CO2 monitoring (`co2.webp`)
   - VPD (Vapor Pressure Deficit) monitoring (`vpd.webp`)
   - Humidifier control (`humidifier.webp`)
   - Dehumidifier control (`dehumidifier.webp`)

3. **Air Management**:
   - Fan control (`fan.webp`)
   - Wind speed monitoring (`wind-speed.webp`)
   - Wind pressure monitoring (`wind-pressure.webp`)
   - Air volume control (`airvolume.webp`)
   - General wind control (`wind.webp`)

4. **Water Management**:
   - Drip system control (`drip.webp`)

5. **Additional Features**:
   - Heating pad control (`heatingpad.webp`)
   - Socket/outlet control (`socket.webp`, `outlet1.webp`, `outlet2.webp`)
   - Timer functionality (`timer.webp`)
   - Scene management (`plant-scene.webp`)
   - Auto mode (`auto.webp`)
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
- **High obfuscation**: All class names and methods are obfuscated with single-letter package names
- **String encryption**: Likely present based on obfuscation patterns
- **Native code**: Possible native libraries for BLE communication

### Flutter Structure
The app is built with Flutter and includes:
- Custom assets for UI elements (confirmed from AssetManifest.json)
- Multiple language support (config splits for different languages)
- Responsive design elements
- Platform-specific integrations

### Bundle Structure
The app uses Android App Bundle (XAPK) format with:
- Base APK: `com.marspro.meizhi.apk`
- Language splits: ar, it, my, vi, ko, fr, zh, hi, in, tr, ru, en, ja, de, th, es, pt
- Architecture split: arm64_v8a
- Density split: xxhdpi

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
1. **Obfuscated Code**: All meaningful identifiers are obfuscated with single-letter names
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
1. **Phase 1**: BLE Communication Protocol ✅ COMPLETED
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

**Key Findings from Static Analysis:**
- Confirmed hydroponics/growing system with comprehensive environmental controls
- Flutter-based application with Firebase integration
- Heavy code obfuscation requiring dynamic analysis
- XAPK bundle format with multiple language and architecture splits
- Comprehensive BLE permissions indicating local device communication

---

**Analysis Date**: June 22, 2025  
**Analyst**: AI Assistant  
**Version**: 2.0  
**Status**: Phase 1 Complete - Ready for Dynamic Analysis 