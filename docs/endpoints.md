# MarsPro API Endpoints Documentation

## Overview

This document tracks the discovered REST API endpoints and BLE communication protocols from the MarsPro Android application.

## REST API Endpoints

### Base URL
- **Production**: `https://api.marspro.com`
- **Development**: `https://dev-api.marspro.com` (if available)

### Authentication

#### Login
- **Endpoint**: `/api/v1/login`
- **Method**: POST
- **Description**: User authentication
- **Request Body**:
  ```json
  {
    "email": "user@example.com",
    "password": "password",
    "device_id": "android_device_id"
  }
  ```
- **Response**:
  ```json
  {
    "success": true,
    "token": "jwt_token_here",
    "user_id": "user_id",
    "expires_at": "2025-12-31T23:59:59Z"
  }
  ```
- **Status**: To be discovered

#### Refresh Token
- **Endpoint**: `/api/v1/refresh`
- **Method**: POST
- **Description**: Refresh authentication token
- **Headers**: `Authorization: Bearer <token>`
- **Status**: To be discovered

### Device Management

#### Get Devices
- **Endpoint**: `/api/v1/devices`
- **Method**: GET
- **Description**: Get user's devices
- **Headers**: `Authorization: Bearer <token>`
- **Response**:
  ```json
  {
    "devices": [
      {
        "id": "device_id",
        "name": "Device Name",
        "type": "light|fan|sensor",
        "mac_address": "AA:BB:CC:DD:EE:FF",
        "status": "online|offline",
        "last_seen": "2025-06-22T18:00:00Z"
      }
    ]
  }
  ```
- **Status**: To be discovered

#### Get Device Details
- **Endpoint**: `/api/v1/devices/{device_id}`
- **Method**: GET
- **Description**: Get detailed device information
- **Headers**: `Authorization: Bearer <token>`
- **Status**: To be discovered

### Device Control

#### Control Device
- **Endpoint**: `/api/v1/devices/{device_id}/control`
- **Method**: POST
- **Description**: Send control command to device
- **Headers**: `Authorization: Bearer <token>`
- **Request Body**:
  ```json
  {
    "command": "turn_on|turn_off|set_brightness|set_color_temp|set_speed",
    "parameters": {
      "brightness": 100,
      "color_temp": 2700,
      "speed": "low|medium|high"
    }
  }
  ```
- **Status**: To be discovered

#### Get Device Status
- **Endpoint**: `/api/v1/devices/{device_id}/status`
- **Method**: GET
- **Description**: Get current device status
- **Headers**: `Authorization: Bearer <token>`
- **Response**:
  ```json
  {
    "device_id": "device_id",
    "power": "on|off",
    "brightness": 100,
    "color_temp": 2700,
    "speed": "low|medium|high",
    "last_updated": "2025-06-22T18:00:00Z"
  }
  ```
- **Status**: To be discovered

### User Management

#### Get User Profile
- **Endpoint**: `/api/v1/user/profile`
- **Method**: GET
- **Description**: Get user profile information
- **Headers**: `Authorization: Bearer <token>`
- **Status**: To be discovered

#### Update User Profile
- **Endpoint**: `/api/v1/user/profile`
- **Method**: PUT
- **Description**: Update user profile
- **Headers**: `Authorization: Bearer <token>`
- **Status**: To be discovered

## BLE Communication

### Service UUIDs
- **Main Service**: To be discovered
- **Control Service**: To be discovered
- **Status Service**: To be discovered

### Characteristics

#### Control Characteristic
- **UUID**: To be discovered
- **Properties**: Write, Write Without Response
- **Description**: Send control commands to device
- **Commands**:
  - Turn On: To be discovered
  - Turn Off: To be discovered
  - Set Brightness: To be discovered
  - Set Color Temperature: To be discovered
  - Set Fan Speed: To be discovered

#### Status Characteristic
- **UUID**: To be discovered
- **Properties**: Read, Notify
- **Description**: Read device status and receive notifications
- **Data Format**: To be discovered

#### Configuration Characteristic
- **UUID**: To be discovered
- **Properties**: Read, Write
- **Description**: Device configuration parameters
- **Status**: To be discovered

### Command Protocol

#### Light Commands
- **Turn On**: To be discovered
- **Turn Off**: To be discovered
- **Set Brightness (0-100)**: To be discovered
- **Set Color Temperature (2200K-6500K)**: To be discovered
- **Set Color (RGB)**: To be discovered

#### Fan Commands
- **Turn On**: To be discovered
- **Turn Off**: To be discovered
- **Set Speed (Low/Medium/High)**: To be discovered
- **Set Mode (Normal/Sleep/Timer)**: To be discovered

#### Sensor Commands
- **Read Temperature**: To be discovered
- **Read Humidity**: To be discovered
- **Read Air Quality**: To be discovered

### Data Formats

#### Command Format
```
[Command ID][Length][Data...][Checksum]
```

#### Response Format
```
[Response ID][Length][Data...][Checksum]
```

#### Status Format
```
[Status ID][Length][Data...][Checksum]
```

## Error Codes

### HTTP Status Codes
- **200**: Success
- **400**: Bad Request
- **401**: Unauthorized
- **403**: Forbidden
- **404**: Not Found
- **429**: Rate Limited
- **500**: Internal Server Error

### BLE Error Codes
- **0x00**: Success
- **0x01**: Invalid Command
- **0x02**: Invalid Parameter
- **0x03**: Device Busy
- **0x04**: Device Offline
- **0xFF**: Unknown Error

## Security

### Authentication
- JWT tokens for REST API
- Device pairing for BLE communication
- Token refresh mechanism

### Encryption
- HTTPS for REST API
- BLE encryption (if supported)

## Rate Limiting
- REST API: To be discovered
- BLE: No rate limiting

## Notes

- All endpoints are subject to discovery during analysis
- BLE communication may vary by device model
- Some features may require cloud API
- Local BLE control provides faster response times

---

*Last Updated: 2025-06-22*
*Status: Discovery in Progress* 