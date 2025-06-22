"""Config flow for MarsPro integration."""

import logging
from typing import Any, Dict, Optional

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_EMAIL, CONF_PASSWORD
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.exceptions import HomeAssistantError

from .api import MarsProAPI
from .const import CONF_BLE_MAC, CONF_USE_CLOUD, DOMAIN

_LOGGER = logging.getLogger(__name__)


class MarsProConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for MarsPro."""

    VERSION = 1

    def __init__(self) -> None:
        """Initialize config flow."""
        self.data: Dict[str, Any] = {}

    async def async_step_user(
        self, user_input: Optional[Dict[str, Any]] = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            try:
                # Store user input
                self.data.update(user_input)
                
                # Test connection
                api = MarsProAPI(
                    email=user_input[CONF_EMAIL],
                    password=user_input[CONF_PASSWORD],
                    use_cloud=user_input.get(CONF_USE_CLOUD, False),
                    ble_mac=user_input.get(CONF_BLE_MAC),
                )
                
                await api.test_connection()
                
                # Create entry
                return self.async_create_entry(
                    title=f"MarsPro ({user_input[CONF_EMAIL]})",
                    data=self.data,
                )
                
            except Exception as ex:
                _LOGGER.error("Config flow error: %s", ex)
                errors["base"] = "cannot_connect"

        # Show form
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_EMAIL): str,
                    vol.Required(CONF_PASSWORD): str,
                    vol.Optional(CONF_USE_CLOUD, default=False): bool,
                    vol.Optional(CONF_BLE_MAC): str,
                }
            ),
            errors=errors,
        )

    async def async_step_reauth(
        self, user_input: Optional[Dict[str, Any]] = None
    ) -> FlowResult:
        """Handle reauthorization."""
        errors = {}

        if user_input is not None:
            try:
                # Test new credentials
                api = MarsProAPI(
                    email=user_input[CONF_EMAIL],
                    password=user_input[CONF_PASSWORD],
                    use_cloud=user_input.get(CONF_USE_CLOUD, False),
                    ble_mac=user_input.get(CONF_BLE_MAC),
                )
                
                await api.test_connection()
                
                # Update entry
                existing_entry = self.hass.config_entries.async_get_entry(
                    self.context["entry_id"]
                )
                if existing_entry:
                    self.hass.config_entries.async_update_entry(
                        existing_entry, data=user_input
                    )
                    await self.hass.config_entries.async_reload(existing_entry.entry_id)
                
                return self.async_abort(reason="reauth_successful")
                
            except Exception as ex:
                _LOGGER.error("Reauth error: %s", ex)
                errors["base"] = "cannot_connect"

        # Show reauth form
        return self.async_show_form(
            step_id="reauth",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_EMAIL): str,
                    vol.Required(CONF_PASSWORD): str,
                    vol.Optional(CONF_USE_CLOUD, default=False): bool,
                    vol.Optional(CONF_BLE_MAC): str,
                }
            ),
            errors=errors,
        )


class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""


class InvalidAuth(HomeAssistantError):
    """Error to indicate there is invalid auth.""" 