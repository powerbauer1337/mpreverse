#!/usr/bin/env python3
"""Direct test script for MarsPro BLE client."""

import asyncio
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import the BLE client directly
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src', 'marspro'))

# Import the standalone BLE client directly
from ble_client_standalone import (
    MarsProBLEClient,
    MarsProDeviceScanner,
    MarsProDevice,
    MarsProDeviceType,
    MarsProFeature,
    MarsProSensorData
)


async def test_ble_client():
    """Test the BLE client functionality."""
    print("Testing MarsPro BLE Client (Direct Import)...")
    
    # Test data structures
    print("\n1. Testing data structures...")
    
    # Test MarsProDevice
    device = MarsProDevice(
        address="00:11:22:33:44:55",
        name="Test MarsPro Device",
        device_type=MarsProDeviceType.CONTROLLER,
        features=[MarsProFeature.LIGHTING, MarsProFeature.CLIMATE],
        firmware_version="1.3.2",
        battery_level=85,
        rssi=-50
    )
    print(f"✓ Created device: {device.name} ({device.address})")
    print(f"  Features: {[f.value for f in device.features]}")
    
    # Test MarsProSensorData
    sensor_data = MarsProSensorData(
        temperature=25.5,
        humidity=60.0,
        co2=400.0,
        vpd=1.2,
        ppfd=500.0,
        wind_speed=2.5,
        wind_pressure=1013.25,
        air_volume=100.0,
        timestamp=1234567890.0
    )
    print(f"✓ Created sensor data: {sensor_data.temperature}°C, {sensor_data.humidity}%")
    
    # Test BLE client initialization
    print("\n2. Testing BLE client initialization...")
    try:
        client = MarsProBLEClient("00:11:22:33:44:55")
        print(f"✓ Created BLE client for device: {client.device_address}")
        print(f"  Service UUID: {client.SERVICE_UUID}")
        print(f"  Command UUID: {client.COMMAND_CHAR_UUID}")
        print(f"  Data UUID: {client.DATA_CHAR_UUID}")
    except Exception as e:
        print(f"✗ Failed to create BLE client: {e}")
        return
    
    # Test command packet building
    print("\n3. Testing command packet building...")
    try:
        # Test light command
        light_packet = client._build_command_packet(client.CMD_SET_LIGHT, {"intensity": 50})
        print(f"✓ Light command packet: {light_packet.hex()}")
        
        # Test temperature command
        temp_packet = client._build_command_packet(client.CMD_SET_TEMPERATURE, {"temperature": 25.0})
        print(f"✓ Temperature command packet: {temp_packet.hex()}")
        
        # Test humidity command
        humidity_packet = client._build_command_packet(client.CMD_SET_HUMIDITY, {"humidity": 60.0})
        print(f"✓ Humidity command packet: {humidity_packet.hex()}")
    except Exception as e:
        print(f"✗ Failed to build command packets: {e}")
    
    # Test sensor data parsing
    print("\n4. Testing sensor data parsing...")
    try:
        test_data = b'\x01\x02\x03\x04\x05\x06\x07\x08'
        parsed_data = client._parse_sensor_data(test_data)
        print(f"✓ Parsed sensor data: {parsed_data.temperature}°C, {parsed_data.humidity}%")
    except Exception as e:
        print(f"✗ Failed to parse sensor data: {e}")
    
    # Test device scanner
    print("\n5. Testing device scanner...")
    try:
        scanner = MarsProDeviceScanner()
        print(f"✓ Created device scanner")
        
        # Test device detection
        from unittest.mock import Mock
        mock_device = Mock()
        mock_device.name = "MarsPro Controller"
        mock_device.address = "00:11:22:33:44:55"
        mock_device.rssi = -50
        
        is_marspro = scanner._is_marspro_device(mock_device)
        print(f"✓ Device detection: {is_marspro}")
        
        # Test device creation
        marspro_device = scanner._create_marspro_device(mock_device)
        print(f"✓ Created MarsPro device: {marspro_device.name}")
    except Exception as e:
        print(f"✗ Failed to test device scanner: {e}")
    
    print("\n6. Testing control methods...")
    try:
        # Test light control
        light_result = await client.control_light("main", 75, 3600)
        print(f"✓ Light control method: {'Success' if light_result else 'Failed'}")
        
        # Test climate control
        climate_result = await client.control_climate(temperature=25.0, humidity=60.0)
        print(f"✓ Climate control method: {'Success' if climate_result else 'Failed'}")
        
        # Test water control
        water_result = await client.control_water(drip_rate=2.5, flow_rate=100.0)
        print(f"✓ Water control method: {'Success' if water_result else 'Failed'}")
    except Exception as e:
        print(f"✗ Failed to test control methods: {e}")
    
    print("\n✅ All tests completed!")


def test_imports():
    """Test that all required modules can be imported."""
    print("Testing imports...")
    
    try:
        import bleak
        print("✓ bleak imported successfully")
    except ImportError:
        print("✗ bleak not available (BLE functionality will be limited)")
    
    try:
        import struct
        print("✓ struct imported successfully")
    except ImportError:
        print("✗ struct import failed")
    
    try:
        import asyncio
        print("✓ asyncio imported successfully")
    except ImportError:
        print("✗ asyncio import failed")
    
    try:
        import logging
        print("✓ logging imported successfully")
    except ImportError:
        print("✗ logging import failed")


if __name__ == "__main__":
    print("MarsPro BLE Client Test Suite (Direct Import)")
    print("=" * 50)
    
    # Test imports first
    test_imports()
    
    # Run async tests
    try:
        asyncio.run(test_ble_client())
    except Exception as e:
        print(f"\n❌ Test suite failed: {e}")
        sys.exit(1) 