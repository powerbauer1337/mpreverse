"""Tests for MarsPro BLE client."""

import pytest
import asyncio
from unittest.mock import Mock, AsyncMock, patch
from src.marspro.ble_client import (
    MarsProBLEClient,
    MarsProDeviceScanner,
    MarsProDevice,
    MarsProDeviceType,
    MarsProFeature,
    MarsProSensorData
)


class TestMarsProBLEClient:
    """Test MarsPro BLE client functionality."""
    
    @pytest.fixture
    def client(self):
        """Create a test client."""
        return MarsProBLEClient("00:11:22:33:44:55")
    
    @pytest.fixture
    def mock_bleak_client(self):
        """Create a mock BleakClient."""
        mock_client = Mock()
        mock_client.connect = AsyncMock()
        mock_client.disconnect = AsyncMock()
        mock_client.get_services = AsyncMock()
        mock_client.read_gatt_char = AsyncMock()
        mock_client.write_gatt_char = AsyncMock()
        mock_client.start_notify = AsyncMock()
        return mock_client
    
    def test_client_initialization(self, client):
        """Test client initialization."""
        assert client.device_address == "00:11:22:33:44:55"
        assert client.client is None
        assert not client.is_connected
        assert client.device_info is None
    
    @pytest.mark.asyncio
    async def test_connect_success(self, client, mock_bleak_client):
        """Test successful connection."""
        with patch('src.marspro.ble_client.BleakClient', return_value=mock_bleak_client):
            # Mock service discovery
            mock_service = Mock()
            mock_service.uuid = "test-service-uuid"
            mock_characteristic = Mock()
            mock_characteristic.uuid = "test-char-uuid"
            mock_characteristic.properties = ["read", "write"]
            mock_service.characteristics = [mock_characteristic]
            mock_bleak_client.get_services.return_value = [mock_service]
            
            result = await client.connect()
            
            assert result is True
            assert client.is_connected
            assert client.client == mock_bleak_client
            mock_bleak_client.connect.assert_called_once()
            mock_bleak_client.get_services.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_connect_failure(self, client, mock_bleak_client):
        """Test connection failure."""
        with patch('src.marspro.ble_client.BleakClient', return_value=mock_bleak_client):
            mock_bleak_client.connect.side_effect = Exception("Connection failed")
            
            result = await client.connect()
            
            assert result is False
            assert not client.is_connected
    
    @pytest.mark.asyncio
    async def test_disconnect(self, client, mock_bleak_client):
        """Test disconnection."""
        with patch('src.marspro.ble_client.BleakClient', return_value=mock_bleak_client):
            # Connect first
            mock_service = Mock()
            mock_service.uuid = "test-service-uuid"
            mock_service.characteristics = []
            mock_bleak_client.get_services.return_value = [mock_service]
            await client.connect()
            
            # Disconnect
            await client.disconnect()
            
            assert not client.is_connected
            mock_bleak_client.disconnect.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_read_device_info(self, client, mock_bleak_client):
        """Test reading device information."""
        with patch('src.marspro.ble_client.BleakClient', return_value=mock_bleak_client):
            # Setup connection
            mock_service = Mock()
            mock_service.uuid = "test-service-uuid"
            mock_characteristic = Mock()
            mock_characteristic.uuid = client.STATUS_CHAR_UUID
            mock_service.characteristics = [mock_characteristic]
            mock_bleak_client.get_services.return_value = [mock_service]
            await client.connect()
            
            # Mock status data
            mock_bleak_client.read_gatt_char.return_value = b'\x01\x02\x03'
            
            device_info = await client.read_device_info()
            
            assert device_info is not None
            assert device_info.name == "MarsPro Controller"
            assert device_info.device_type == MarsProDeviceType.CONTROLLER
            assert MarsProFeature.LIGHTING in device_info.features
            mock_bleak_client.read_gatt_char.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_read_sensor_data(self, client, mock_bleak_client):
        """Test reading sensor data."""
        with patch('src.marspro.ble_client.BleakClient', return_value=mock_bleak_client):
            # Setup connection
            mock_service = Mock()
            mock_service.uuid = "test-service-uuid"
            mock_characteristic = Mock()
            mock_characteristic.uuid = client.DATA_CHAR_UUID
            mock_service.characteristics = [mock_characteristic]
            mock_bleak_client.get_services.return_value = [mock_service]
            await client.connect()
            
            # Mock sensor data
            mock_bleak_client.read_gatt_char.return_value = b'\x01\x02\x03'
            
            sensor_data = await client.read_sensor_data()
            
            assert sensor_data is not None
            assert sensor_data.temperature == 25.5
            assert sensor_data.humidity == 60.0
            mock_bleak_client.read_gatt_char.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_send_command(self, client, mock_bleak_client):
        """Test sending commands."""
        with patch('src.marspro.ble_client.BleakClient', return_value=mock_bleak_client):
            # Setup connection
            mock_service = Mock()
            mock_service.uuid = "test-service-uuid"
            mock_characteristic = Mock()
            mock_characteristic.uuid = client.COMMAND_CHAR_UUID
            mock_service.characteristics = [mock_characteristic]
            mock_bleak_client.get_services.return_value = [mock_service]
            await client.connect()
            
            # Send command
            result = await client.send_command(client.CMD_SET_LIGHT, {"intensity": 50})
            
            assert result is True
            mock_bleak_client.write_gatt_char.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_control_light(self, client, mock_bleak_client):
        """Test light control."""
        with patch('src.marspro.ble_client.BleakClient', return_value=mock_bleak_client):
            # Setup connection
            mock_service = Mock()
            mock_service.uuid = "test-service-uuid"
            mock_characteristic = Mock()
            mock_characteristic.uuid = client.COMMAND_CHAR_UUID
            mock_service.characteristics = [mock_characteristic]
            mock_bleak_client.get_services.return_value = [mock_service]
            await client.connect()
            
            # Control light
            result = await client.control_light("main", 75, 3600)
            
            assert result is True
            mock_bleak_client.write_gatt_char.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_control_climate(self, client, mock_bleak_client):
        """Test climate control."""
        with patch('src.marspro.ble_client.BleakClient', return_value=mock_bleak_client):
            # Setup connection
            mock_service = Mock()
            mock_service.uuid = "test-service-uuid"
            mock_characteristic = Mock()
            mock_characteristic.uuid = client.COMMAND_CHAR_UUID
            mock_service.characteristics = [mock_characteristic]
            mock_bleak_client.get_services.return_value = [mock_service]
            await client.connect()
            
            # Control climate
            result = await client.control_climate(temperature=25.0, humidity=60.0, fan_speed=3)
            
            assert result is True
            mock_bleak_client.write_gatt_char.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_control_water(self, client, mock_bleak_client):
        """Test water control."""
        with patch('src.marspro.ble_client.BleakClient', return_value=mock_bleak_client):
            # Setup connection
            mock_service = Mock()
            mock_service.uuid = "test-service-uuid"
            mock_characteristic = Mock()
            mock_characteristic.uuid = client.COMMAND_CHAR_UUID
            mock_service.characteristics = [mock_characteristic]
            mock_bleak_client.get_services.return_value = [mock_service]
            await client.connect()
            
            # Control water
            result = await client.control_water(drip_rate=2.5, flow_rate=100.0)
            
            assert result is True
            mock_bleak_client.write_gatt_char.assert_called_once()
    
    def test_build_command_packet(self, client):
        """Test command packet building."""
        # Test light command
        packet = client._build_command_packet(client.CMD_SET_LIGHT, {"intensity": 50})
        assert len(packet) > 0
        assert packet[0] == client.CMD_SET_LIGHT
        
        # Test temperature command
        packet = client._build_command_packet(client.CMD_SET_TEMPERATURE, {"temperature": 25.0})
        assert len(packet) > 0
        assert packet[0] == client.CMD_SET_TEMPERATURE
        
        # Test humidity command
        packet = client._build_command_packet(client.CMD_SET_HUMIDITY, {"humidity": 60.0})
        assert len(packet) > 0
        assert packet[0] == client.CMD_SET_HUMIDITY
    
    def test_parse_sensor_data(self, client):
        """Test sensor data parsing."""
        test_data = b'\x01\x02\x03\x04'
        sensor_data = client._parse_sensor_data(test_data)
        
        assert sensor_data is not None
        assert sensor_data.temperature == 25.5
        assert sensor_data.humidity == 60.0
        assert sensor_data.co2 == 400.0
        assert sensor_data.vpd == 1.2
        assert sensor_data.ppfd == 500.0


class TestMarsProDeviceScanner:
    """Test MarsPro device scanner functionality."""
    
    @pytest.fixture
    def scanner(self):
        """Create a test scanner."""
        return MarsProDeviceScanner()
    
    @pytest.fixture
    def mock_bleak_scanner(self):
        """Create a mock BleakScanner."""
        mock_scanner = Mock()
        mock_scanner.discover = AsyncMock()
        return mock_scanner
    
    def test_scanner_initialization(self, scanner):
        """Test scanner initialization."""
        assert scanner.discovered_devices == []
    
    @pytest.mark.asyncio
    async def test_scan_for_devices(self, scanner, mock_bleak_scanner):
        """Test device scanning."""
        with patch('src.marspro.ble_client.BleakScanner', return_value=mock_bleak_scanner):
            # Mock discovered devices
            mock_device1 = Mock()
            mock_device1.address = "00:11:22:33:44:55"
            mock_device1.name = "MarsPro Controller"
            mock_device1.rssi = -50
            
            mock_device2 = Mock()
            mock_device2.address = "00:11:22:33:44:66"
            mock_device2.name = "Other Device"
            mock_device2.rssi = -60
            
            mock_bleak_scanner.discover.return_value = [mock_device1, mock_device2]
            
            devices = await scanner.scan_for_devices(timeout=5.0)
            
            assert len(devices) == 1
            assert devices[0].name == "MarsPro Controller"
            assert devices[0].address == "00:11:22:33:44:55"
            mock_bleak_scanner.discover.assert_called_once_with(timeout=5.0)
    
    def test_is_marspro_device(self, scanner):
        """Test MarsPro device detection."""
        # Test MarsPro device
        mock_device = Mock()
        mock_device.name = "MarsPro Controller"
        assert scanner._is_marspro_device(mock_device) is True
        
        # Test Mars device
        mock_device.name = "Mars Grow Light"
        assert scanner._is_marspro_device(mock_device) is True
        
        # Test other device
        mock_device.name = "Other Device"
        assert scanner._is_marspro_device(mock_device) is False
        
        # Test None name
        mock_device.name = None
        assert scanner._is_marspro_device(mock_device) is False
    
    def test_create_marspro_device(self, scanner):
        """Test MarsPro device creation."""
        mock_device = Mock()
        mock_device.address = "00:11:22:33:44:55"
        mock_device.name = "Test Device"
        mock_device.rssi = -50
        
        marspro_device = scanner._create_marspro_device(mock_device)
        
        assert marspro_device.address == "00:11:22:33:44:55"
        assert marspro_device.name == "Test Device"
        assert marspro_device.device_type == MarsProDeviceType.CONTROLLER
        assert marspro_device.rssi == -50
    
    def test_get_discovered_devices(self, scanner):
        """Test getting discovered devices."""
        # Add some test devices
        test_device = MarsProDevice(
            address="00:11:22:33:44:55",
            name="Test Device",
            device_type=MarsProDeviceType.CONTROLLER,
            features=[MarsProFeature.LIGHTING]
        )
        scanner.discovered_devices.append(test_device)
        
        devices = scanner.get_discovered_devices()
        
        assert len(devices) == 1
        assert devices[0].name == "Test Device"


class TestMarsProDataStructures:
    """Test MarsPro data structures."""
    
    def test_marspro_device(self):
        """Test MarsProDevice dataclass."""
        device = MarsProDevice(
            address="00:11:22:33:44:55",
            name="Test Device",
            device_type=MarsProDeviceType.CONTROLLER,
            features=[MarsProFeature.LIGHTING, MarsProFeature.CLIMATE],
            firmware_version="1.3.2",
            battery_level=85,
            rssi=-50
        )
        
        assert device.address == "00:11:22:33:44:55"
        assert device.name == "Test Device"
        assert device.device_type == MarsProDeviceType.CONTROLLER
        assert len(device.features) == 2
        assert MarsProFeature.LIGHTING in device.features
        assert MarsProFeature.CLIMATE in device.features
        assert device.firmware_version == "1.3.2"
        assert device.battery_level == 85
        assert device.rssi == -50
    
    def test_marspro_sensor_data(self):
        """Test MarsProSensorData dataclass."""
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
        
        assert sensor_data.temperature == 25.5
        assert sensor_data.humidity == 60.0
        assert sensor_data.co2 == 400.0
        assert sensor_data.vpd == 1.2
        assert sensor_data.ppfd == 500.0
        assert sensor_data.wind_speed == 2.5
        assert sensor_data.wind_pressure == 1013.25
        assert sensor_data.air_volume == 100.0
        assert sensor_data.timestamp == 1234567890.0


if __name__ == "__main__":
    pytest.main([__file__]) 