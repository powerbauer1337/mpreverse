"""Light platform for MarsPro integration."""

import logging
from typing import Any, Dict, Optional

from homeassistant.components.light import (
    ATTR_BRIGHTNESS,
    ATTR_COLOR_TEMP,
    ATTR_RGB_COLOR,
    ColorMode,
    LightEntity,
    LightEntityFeature,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from .const import (
    CMD_POWER_OFF,
    CMD_POWER_ON,
    CMD_SET_BRIGHTNESS,
    CMD_SET_COLOR,
    DEVICE_TYPE_LIGHT,
    DOMAIN,
    STATUS_OFF,
    STATUS_ON,
)
from .coordinator import MarsProDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up MarsPro light based on a config entry."""
    coordinator: MarsProDataUpdateCoordinator = hass.data[DOMAIN][config_entry.entry_id]

    # Get light devices
    light_devices = coordinator.get_devices_by_type(DEVICE_TYPE_LIGHT)
    
    entities = []
    for device in light_devices:
        entities.append(MarsProLight(coordinator, device))
    
    if entities:
        async_add_entities(entities)


class MarsProLight(LightEntity):
    """Representation of a MarsPro light."""

    def __init__(
        self, coordinator: MarsProDataUpdateCoordinator, device: Dict[str, Any]
    ) -> None:
        """Initialize the light."""
        self.coordinator = coordinator
        self.device = device
        self.device_id = device.get("id")
        self._attr_name = device.get("name", f"MarsPro Light {self.device_id}")
        self._attr_unique_id = f"{DOMAIN}_{self.device_id}"
        
        # Set supported features
        self._attr_supported_color_modes = {ColorMode.BRIGHTNESS}
        self._attr_color_mode = ColorMode.BRIGHTNESS
        
        # Initialize state
        self._attr_brightness = 255
        self._attr_is_on = False

    @property
    def device_info(self) -> DeviceInfo:
        """Return device info."""
        return DeviceInfo(
            identifiers={(DOMAIN, self.device_id)},
            name=self._attr_name,
            manufacturer="MarsPro",
            model=self.device.get("model", "Unknown"),
            sw_version=self.device.get("firmware_version", "Unknown"),
        )

    @property
    def should_poll(self) -> bool:
        """No polling needed."""
        return False

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return self.coordinator.last_update_success

    async def async_added_to_hass(self) -> None:
        """When entity is added to hass."""
        await super().async_added_to_hass()
        self.async_on_remove(
            self.coordinator.async_add_listener(self._handle_coordinator_update)
        )

    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        device_data = self.coordinator.get_device(self.device_id)
        if device_data:
            self._update_from_device_data(device_data)
            self.async_write_ha_state()

    def _update_from_device_data(self, device_data: Dict[str, Any]) -> None:
        """Update entity state from device data."""
        # Update power state
        power = device_data.get("power", STATUS_OFF)
        self._attr_is_on = power == STATUS_ON
        
        # Update brightness
        brightness = device_data.get("brightness", 100)
        self._attr_brightness = int((brightness / 100) * 255)

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the light on."""
        try:
            # Send power on command
            await self.coordinator.send_command(self.device_id, CMD_POWER_ON)
            
            # Handle brightness
            if ATTR_BRIGHTNESS in kwargs:
                brightness = int((kwargs[ATTR_BRIGHTNESS] / 255) * 100)
                await self.coordinator.send_command(
                    self.device_id, CMD_SET_BRIGHTNESS, brightness=brightness
                )
            
            # Handle color (if supported)
            if ATTR_RGB_COLOR in kwargs:
                rgb_color = kwargs[ATTR_RGB_COLOR]
                await self.coordinator.send_command(
                    self.device_id, CMD_SET_COLOR, rgb_color=rgb_color
                )
            
            # Refresh data
            await self.coordinator.async_request_refresh()
            
        except Exception as ex:
            _LOGGER.error("Failed to turn on light %s: %s", self.device_id, ex)
            raise

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the light off."""
        try:
            await self.coordinator.send_command(self.device_id, CMD_POWER_OFF)
            await self.coordinator.async_request_refresh()
        except Exception as ex:
            _LOGGER.error("Failed to turn off light %s: %s", self.device_id, ex)
            raise 