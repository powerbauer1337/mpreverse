# MarsPro BLE Communication Protocol Documentation

## Overview

This document describes the Bluetooth Low Energy (BLE) communication protocol used by MarsPro devices. This protocol enables local control of MarsPro hydroponics systems without cloud dependency.

## Device Information

### Device Characteristics
- **Device Type**: MarsPro Hydroponics Controller
- **Communication Protocol**: Bluetooth Low Energy (BLE)
- **Supported Features**: Environmental control, sensor monitoring, automation

### Device Discovery
- **Advertising Name**: [To be discovered during analysis]
- **Service UUIDs**: [To be discovered during analysis]
- **Manufacturer Data**: [To be discovered during analysis]

## BLE Service Structure

### Primary Service
```
Service UUID: [To be discovered]
Description: Main control service for MarsPro device
```

#### Characteristics

##### Device Information
```
Characteristic UUID: [To be discovered]
Properties: Read
Description: Device information and status
Data Format: [To be discovered]
```

##### Control Commands
```
Characteristic UUID: [To be discovered]
Properties: Write
Description: Send control commands to device
Data Format: [To be discovered]
```

##### Sensor Data
```
Characteristic UUID: [To be discovered]
Properties: Read, Notify
Description: Real-time sensor data
Data Format: [To be discovered]
```

##### Configuration
```
Characteristic UUID: [To be discovered]
Properties: Read, Write
Description: Device configuration parameters
Data Format: [To be discovered]
```

## Command Protocol

### Command Structure
```
[Header] [Command ID] [Data Length] [Data] [Checksum]
```

### Command Types

#### Light Control
```
Command ID: [To be discovered]
Description: Control lighting systems
Parameters:
  - Light Type (UV, PPFD, Vegetative, General)
  - Intensity (0-100%)
  - Duration (minutes)
  - Mode (Manual, Auto, Timer)
```

#### Climate Control
```
Command ID: [To be discovered]
Description: Control climate systems
Parameters:
  - Temperature Setpoint
  - Humidity Setpoint
  - Fan Speed
  - CO2 Level
```

#### Water Management
```
Command ID: [To be discovered]
Description: Control water systems
Parameters:
  - Drip Rate
  - Water Flow
  - Timer Settings
```

#### System Control
```
Command ID: [To be discovered]
Description: System-level commands
Parameters:
  - Power On/Off
  - Reset
  - Factory Reset
  - Firmware Update
```

## Data Formats

### Sensor Data Format
```
[Timestamp] [Sensor ID] [Value] [Unit] [Status]
```

### Status Response Format
```
[Device ID] [Status] [Error Code] [Additional Data]
```

### Configuration Format
```
[Parameter ID] [Value] [Validation]
```

## Error Codes

| Code | Description |
|------|-------------|
| [To be discovered] | [To be discovered] |
| [To be discovered] | [To be discovered] |
| [To be discovered] | [To be discovered] |

## Security

### Authentication
- **Method**: [To be discovered]
- **Key Exchange**: [To be discovered]
- **Encryption**: [To be discovered]

### Pairing Process
1. [To be discovered]
2. [To be discovered]
3. [To be discovered]

## Implementation Examples

### Python Example (using bleak)
```python
import asyncio
from bleak import BleakClient, BleakScanner

class MarsProClient:
    def __init__(self, device_address):
        self.device_address = device_address
        self.client = None
    
    async def connect(self):
        self.client = BleakClient(self.device_address)
        await self.client.connect()
    
    async def discover_services(self):
        services = await self.client.get_services()
        for service in services:
            print(f"Service: {service.uuid}")
            for char in service.characteristics:
                print(f"  Characteristic: {char.uuid}")
    
    async def read_sensor_data(self):
        # [To be implemented based on discovered UUIDs]
        pass
    
    async def send_control_command(self, command):
        # [To be implemented based on discovered UUIDs]
        pass
```

### Home Assistant Integration
```python
# Example Home Assistant sensor entity
class MarsProSensor(SensorEntity):
    def __init__(self, coordinator, device_id, sensor_type):
        self.coordinator = coordinator
        self.device_id = device_id
        self.sensor_type = sensor_type
    
    @property
    def name(self):
        return f"MarsPro {self.sensor_type}"
    
    @property
    def state(self):
        return self.coordinator.data.get(self.sensor_type)
```

## Testing

### Test Commands
```
# Test light control
[Command to be discovered]

# Test sensor reading
[Command to be discovered]

# Test configuration
[Command to be discovered]
```

### Validation
- [ ] Device discovery works
- [ ] Connection establishment successful
- [ ] Service discovery returns expected UUIDs
- [ ] Command sending works
- [ ] Data reading works
- [ ] Error handling works

## Troubleshooting

### Common Issues
1. **Connection Failed**
   - Check device is in range
   - Verify device is advertising
   - Check permissions

2. **Commands Not Working**
   - Verify characteristic UUIDs
   - Check data format
   - Verify device state

3. **Data Not Updating**
   - Check notification subscription
   - Verify characteristic properties
   - Check device status

## Future Enhancements

### Planned Features
- [ ] Multi-device support
- [ ] Advanced automation
- [ ] Data logging
- [ ] Remote access
- [ ] Firmware updates

### API Extensions
- [ ] REST API wrapper
- [ ] MQTT integration
- [ ] WebSocket support
- [ ] GraphQL interface

---

**Document Version**: 1.0  
**Last Updated**: [Date]  
**Status**: In Progress (Dynamic Analysis Required) 