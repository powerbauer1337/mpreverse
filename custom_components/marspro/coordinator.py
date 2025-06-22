"""Data coordinator for MarsPro integration."""

import asyncio
import logging
from datetime import timedelta
from typing import Any, Dict, List

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import MarsProAPI
from .const import DEFAULT_SCAN_INTERVAL

_LOGGER = logging.getLogger(__name__)


class MarsProDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching MarsPro data."""

    def __init__(self, hass: HomeAssistant, api: MarsProAPI) -> None:
        """Initialize coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name="MarsPro",
            update_interval=timedelta(seconds=DEFAULT_SCAN_INTERVAL),
        )
        self.api = api
        self.devices: Dict[str, Dict[str, Any]] = {}

    async def _async_update_data(self) -> Dict[str, Any]:
        """Update data via API."""
        try:
            # Get devices
            devices = await self.api.get_devices()
            
            # Update device status
            updated_devices = {}
            for device in devices:
                device_id = device.get("id")
                if device_id:
                    try:
                        status = await self.api.get_device_status(device_id)
                        device.update(status)
                        updated_devices[device_id] = device
                    except Exception as ex:
                        _LOGGER.warning("Failed to get status for device %s: %s", device_id, ex)
                        # Keep existing device data if status update fails
                        if device_id in self.devices:
                            updated_devices[device_id] = self.devices[device_id]
                        else:
                            updated_devices[device_id] = device
            
            self.devices = updated_devices
            
            return {
                "devices": updated_devices,
                "last_update": asyncio.get_event_loop().time(),
            }
            
        except Exception as ex:
            _LOGGER.error("Failed to update MarsPro data: %s", ex)
            raise UpdateFailed(f"Failed to update MarsPro data: {ex}") from ex

    async def send_command(self, device_id: str, command: str, **kwargs: Any) -> Dict[str, Any]:
        """Send command to device."""
        try:
            result = await self.api.send_command(device_id, command, **kwargs)
            
            # Refresh data after command
            await self.async_request_refresh()
            
            return result
        except Exception as ex:
            _LOGGER.error("Failed to send command %s to device %s: %s", command, device_id, ex)
            raise

    def get_device(self, device_id: str) -> Dict[str, Any]:
        """Get device data."""
        return self.devices.get(device_id, {})

    def get_devices(self) -> List[Dict[str, Any]]:
        """Get all devices."""
        return list(self.devices.values())

    def get_devices_by_type(self, device_type: str) -> List[Dict[str, Any]]:
        """Get devices by type."""
        return [
            device for device in self.devices.values()
            if device.get("type") == device_type
        ] 