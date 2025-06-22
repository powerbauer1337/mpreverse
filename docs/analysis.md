# MarsPro App Analysis Report

## Overview
- **App Name**: MarsPro
- **Package**: com.marspro.meizhi
- **Version**: 1.3.2 (version code 11)
- **Platform**: Android (Flutter-based)
- **Min SDK**: 23 (Android 6.0)
- **Target SDK**: 34 (Android 14)

## Architecture Analysis

### Technology Stack
- **Framework**: Flutter (Dart-based cross-platform)
- **BLE Library**: `com.signify.hue.flutterreactiveble` (RxAndroidBle wrapper)
- **Authentication**: Firebase Auth
- **Analytics**: Firebase Analytics (disabled by default)
- **Crash Reporting**: Firebase Crashlytics
- **Notifications**: Flutter Local Notifications

### Key Permissions
```xml
<!-- Network & Internet -->
<uses-permission android:name="android.permission.INTERNET"/>
<uses-permission android:name="android.permission.ACCESS_NETWORK_STATE"/>
<uses-permission android:name="android.permission.ACCESS_WIFI_STATE"/>

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
```

## Communication Protocols

### Bluetooth Low Energy (BLE)
The app uses the `flutter_reactive_ble` library which is a Flutter wrapper around RxAndroidBle. Key findings:

#### BLE Operations Identified:
- `readCharacteristic()` - Reading device characteristics
- `writeCharacteristicWithResponse()` - Writing with acknowledgment
- `writeCharacteristicWithoutResponse()` - Writing without acknowledgment
- `setCharacteristicNotification()` - Enabling notifications

#### Standard BLE UUIDs Found:
- `00000000-0000-1000-8000-00805F9B34FB` - Generic service UUID
- `00002902-0000-1000-8000-00805f9b34fb` - Client Characteristic Configuration Descriptor

### Network Communication
- **HTTP/HTTPS**: App has internet permission and uses cleartext traffic
- **Firebase Services**: Authentication, Analytics, Crashlytics
- **Google Services**: Play Services integration

## Code Obfuscation
The app is heavily obfuscated with:
- Short package names (e.g., `y6`, `x5`, `w5`)
- Obfuscated class and method names
- Standard Flutter obfuscation techniques

## Security Analysis

### SSL/TLS
- App allows cleartext traffic (`android:usesCleartextTraffic="true"`)
- May use SSL pinning (common in IoT apps)

### Authentication
- Firebase Authentication integration
- Google Sign-In support
- Custom authentication flow

## Reverse Engineering Challenges

### Static Analysis Limitations
1. **Heavy Obfuscation**: Makes manual code analysis difficult
2. **Flutter Framework**: Native code is minimal, most logic is in Dart
3. **Library Dependencies**: Heavy reliance on third-party libraries

### Recommended Approach
1. **Dynamic Analysis**: Use Frida for runtime analysis
2. **Network Interception**: MITM proxy for API discovery
3. **BLE Traffic Analysis**: Capture BLE communication patterns
4. **Flutter Decompilation**: Extract Dart code if possible

## Next Steps for Home Assistant Integration

### Phase 1: Dynamic Analysis
1. Set up Frida hooks for BLE operations
2. Capture network traffic with mitmproxy
3. Identify device-specific UUIDs and commands

### Phase 2: Protocol Reverse Engineering
1. Map BLE service and characteristic UUIDs
2. Understand command structure and payloads
3. Document authentication mechanisms

### Phase 3: Home Assistant Implementation
1. Create BLE-based integration using `bleak`
2. Implement device discovery and pairing
3. Create light/fan entities with proper state management

## Estimated Complexity
- **BLE Protocol**: Medium (standard BLE patterns)
- **Authentication**: Medium (likely token-based)
- **Device Control**: Medium (standard IoT patterns)
- **Integration Effort**: High (due to obfuscation)

## Recommendations
1. Focus on dynamic analysis over static analysis
2. Use Frida for runtime BLE traffic capture
3. Implement both BLE and cloud API support
4. Create comprehensive error handling for device communication

---

*Last Updated: 2025-06-22*
*Analysis Status: Phase 1 Complete* 