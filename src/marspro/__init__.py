"""The MarsPro integration for Home Assistant."""
from __future__ import annotations

import asyncio
import logging
from typing import Any

import voluptuous as vol

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_EMAIL, CONF_PASSWORD, Platform
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady

from .const import (
    CONF_BLE_MAC,
    CONF_USE_CLOUD,
    DOMAIN,
    PLATFORMS,
)
from .api import MarsProAPI
from .coordinator import MarsProDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {
                vol.Required(CONF_EMAIL): str,
                vol.Required(CONF_PASSWORD): str,
                vol.Optional(CONF_USE_CLOUD, default=False): bool,
                vol.Optional(CONF_BLE_MAC): str,
            }
        )
    }
)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up MarsPro from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    # Create API instance
    api = MarsProAPI(
        email=entry.data[CONF_EMAIL],
        password=entry.data[CONF_PASSWORD],
        use_cloud=entry.data.get(CONF_USE_CLOUD, False),
        ble_mac=entry.data.get(CONF_BLE_MAC),
    )

    # Test connection
    try:
        await api.test_connection()
    except Exception as ex:
        _LOGGER.error("Failed to connect to MarsPro: %s", ex)
        raise ConfigEntryNotReady from ex

    # Create coordinator
    coordinator = MarsProDataUpdateCoordinator(hass, api)
    await coordinator.async_config_entry_first_refresh()

    # Store coordinator
    hass.data[DOMAIN][entry.entry_id] = coordinator

    # Set up platforms
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        coordinator = hass.data[DOMAIN].pop(entry.entry_id)
        await coordinator.api.disconnect()

    return unload_ok


async def async_migrate_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Migrate old entry."""
    _LOGGER.debug("Migrating from version %s", config_entry.version)

    if config_entry.version == 1:
        # Add new config options
        new_data = {**config_entry.data}
        new_data[CONF_USE_CLOUD] = False
        
        config_entry.version = 2
        hass.config_entries.async_update_entry(config_entry, data=new_data)

    _LOGGER.info("Migration to version %s successful", config_entry.version)

    return True 