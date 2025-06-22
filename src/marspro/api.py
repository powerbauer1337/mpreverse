"""API client for MarsPro integration."""

import asyncio
import logging
from typing import Any, Dict, List, Optional

import aiohttp
from bleak import BleakClient, BleakScanner
from bleak.exc import BleakError

from .const import (
    API_BASE_URL,
    API_VERSION,
    BLE_SERVICE_UUID,
    BLE_CHARACTERISTIC_UUID,
    DEFAULT_TIMEOUT,
    ERROR_CONNECTION_FAILED,
    ERROR_AUTHENTICATION_FAILED,
    ERROR_DEVICE_NOT_FOUND,
    ERROR_COMMAND_FAILED,
)

_LOGGER = logging.getLogger(__name__)


class MarsProAPI:
    """API client for MarsPro devices."""

    def __init__(
        self,
        email: str,
        password: str,
        use_cloud: bool = False,
        ble_mac: Optional[str] = None,
    ) -> None:
        """Initialize the API client."""
        self.email = email
        self.password = password
        self.use_cloud = use_cloud
        self.ble_mac = ble_mac
        self.session: Optional[aiohttp.ClientSession] = None
        self.ble_client: Optional[BleakClient] = None
        self.auth_token: Optional[str] = None
        self.devices: Dict[str, Dict[str, Any]] = {}

    async def test_connection(self) -> bool:
        """Test the connection to MarsPro."""
        try:
            if self.use_cloud:
                return await self._test_cloud_connection()
            else:
                return await self._test_ble_connection()
        except Exception as ex:
            _LOGGER.error("Connection test failed: %s", ex)
            raise

    async def _test_cloud_connection(self) -> bool:
        """Test cloud API connection."""
        if not self.session:
            self.session = aiohttp.ClientSession()

        try:
            # Try to authenticate
            await self._authenticate()
            return True
        except Exception as ex:
            _LOGGER.error("Cloud connection test failed: %s", ex)
            return False

    async def _test_ble_connection(self) -> bool:
        """Test BLE connection."""
        if not self.ble_mac:
            _LOGGER.error("BLE MAC address required for local connection")
            return False

        try:
            # Try to connect to the device
            await self._connect_ble()
            return True
        except Exception as ex:
            _LOGGER.error("BLE connection test failed: %s", ex)
            return False

    async def _authenticate(self) -> None:
        """Authenticate with the cloud API."""
        if not self.session:
            raise RuntimeError("Session not initialized")

        auth_data = {
            "email": self.email,
            "password": self.password,
        }

        try:
            async with self.session.post(
                f"{API_BASE_URL}/{API_VERSION}/auth/login",
                json=auth_data,
                timeout=aiohttp.ClientTimeout(total=DEFAULT_TIMEOUT),
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    self.auth_token = data.get("token")
                    if not self.auth_token:
                        raise ValueError("No auth token in response")
                else:
                    raise ValueError(f"Authentication failed: {response.status}")
        except Exception as ex:
            _LOGGER.error("Authentication failed: %s", ex)
            raise

    async def _connect_ble(self) -> None:
        """Connect to device via BLE."""
        if not self.ble_mac:
            raise ValueError("BLE MAC address not provided")

        try:
            self.ble_client = BleakClient(self.ble_mac)
            await self.ble_client.connect(timeout=DEFAULT_TIMEOUT)
            _LOGGER.info("Connected to MarsPro device via BLE")
        except BleakError as ex:
            _LOGGER.error("BLE connection failed: %s", ex)
            raise

    async def get_devices(self) -> List[Dict[str, Any]]:
        """Get list of devices."""
        if self.use_cloud:
            return await self._get_devices_cloud()
        else:
            return await self._get_devices_ble()

    async def _get_devices_cloud(self) -> List[Dict[str, Any]]:
        """Get devices from cloud API."""
        if not self.session or not self.auth_token:
            await self._authenticate()

        headers = {"Authorization": f"Bearer {self.auth_token}"}

        try:
            async with self.session.get(
                f"{API_BASE_URL}/{API_VERSION}/devices",
                headers=headers,
                timeout=aiohttp.ClientTimeout(total=DEFAULT_TIMEOUT),
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get("devices", [])
                else:
                    raise ValueError(f"Failed to get devices: {response.status}")
        except Exception as ex:
            _LOGGER.error("Failed to get devices from cloud: %s", ex)
            raise

    async def _get_devices_ble(self) -> List[Dict[str, Any]]:
        """Get device info via BLE."""
        if not self.ble_client or not self.ble_client.is_connected:
            await self._connect_ble()

        try:
            # Read device information characteristic
            device_info = await self.ble_client.read_gatt_char(BLE_CHARACTERISTIC_UUID)
            
            # Parse device info (format to be discovered)
            device = {
                "id": self.ble_mac,
                "name": f"MarsPro Device ({self.ble_mac})",
                "type": "light",  # Default type
                "status": "online",
                "mac": self.ble_mac,
            }
            
            return [device]
        except Exception as ex:
            _LOGGER.error("Failed to get device info via BLE: %s", ex)
            raise

    async def send_command(
        self, device_id: str, command: str, **kwargs: Any
    ) -> Dict[str, Any]:
        """Send command to device."""
        if self.use_cloud:
            return await self._send_command_cloud(device_id, command, **kwargs)
        else:
            return await self._send_command_ble(device_id, command, **kwargs)

    async def _send_command_cloud(
        self, device_id: str, command: str, **kwargs: Any
    ) -> Dict[str, Any]:
        """Send command via cloud API."""
        if not self.session or not self.auth_token:
            await self._authenticate()

        headers = {"Authorization": f"Bearer {self.auth_token}"}
        payload = {
            "device_id": device_id,
            "command": command,
            **kwargs,
        }

        try:
            async with self.session.post(
                f"{API_BASE_URL}/{API_VERSION}/devices/{device_id}/control",
                json=payload,
                headers=headers,
                timeout=aiohttp.ClientTimeout(total=DEFAULT_TIMEOUT),
            ) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    raise ValueError(f"Command failed: {response.status}")
        except Exception as ex:
            _LOGGER.error("Failed to send command via cloud: %s", ex)
            raise

    async def _send_command_ble(
        self, device_id: str, command: str, **kwargs: Any
    ) -> Dict[str, Any]:
        """Send command via BLE."""
        if not self.ble_client or not self.ble_client.is_connected:
            await self._connect_ble()

        try:
            # Build command payload (format to be discovered)
            payload = self._build_ble_command(command, **kwargs)
            
            # Send command
            await self.ble_client.write_gatt_char(
                BLE_CHARACTERISTIC_UUID, payload, response=True
            )
            
            return {"status": "success", "command": command}
        except Exception as ex:
            _LOGGER.error("Failed to send command via BLE: %s", ex)
            raise

    def _build_ble_command(self, command: str, **kwargs: Any) -> bytes:
        """Build BLE command payload."""
        # This is a placeholder implementation
        # The actual command format needs to be discovered through analysis
        
        if command == "power_on":
            return b"\x01\x01"  # Example: turn on
        elif command == "power_off":
            return b"\x01\x00"  # Example: turn off
        elif command == "set_brightness":
            brightness = kwargs.get("brightness", 100)
            return bytes([0x02, brightness])  # Example: set brightness
        else:
            raise ValueError(f"Unknown command: {command}")

    async def get_device_status(self, device_id: str) -> Dict[str, Any]:
        """Get device status."""
        if self.use_cloud:
            return await self._get_device_status_cloud(device_id)
        else:
            return await self._get_device_status_ble(device_id)

    async def _get_device_status_cloud(self, device_id: str) -> Dict[str, Any]:
        """Get device status from cloud API."""
        if not self.session or not self.auth_token:
            await self._authenticate()

        headers = {"Authorization": f"Bearer {self.auth_token}"}

        try:
            async with self.session.get(
                f"{API_BASE_URL}/{API_VERSION}/devices/{device_id}/status",
                headers=headers,
                timeout=aiohttp.ClientTimeout(total=DEFAULT_TIMEOUT),
            ) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    raise ValueError(f"Failed to get status: {response.status}")
        except Exception as ex:
            _LOGGER.error("Failed to get device status from cloud: %s", ex)
            raise

    async def _get_device_status_ble(self, device_id: str) -> Dict[str, Any]:
        """Get device status via BLE."""
        if not self.ble_client or not self.ble_client.is_connected:
            await self._connect_ble()

        try:
            # Read status characteristic
            status_data = await self.ble_client.read_gatt_char(BLE_CHARACTERISTIC_UUID)
            
            # Parse status (format to be discovered)
            status = {
                "power": "on" if status_data[0] == 1 else "off",
                "brightness": status_data[1] if len(status_data) > 1 else 100,
                "online": True,
            }
            
            return status
        except Exception as ex:
            _LOGGER.error("Failed to get device status via BLE: %s", ex)
            raise

    async def disconnect(self) -> None:
        """Disconnect from API."""
        if self.session:
            await self.session.close()
            self.session = None

        if self.ble_client and self.ble_client.is_connected:
            await self.ble_client.disconnect()
            self.ble_client = None 