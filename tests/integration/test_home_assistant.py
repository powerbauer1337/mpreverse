"""
Integration tests for Home Assistant integration.
"""

import pytest
from unittest.mock import AsyncMock, patch
from homeassistant.core import HomeAssistant
from homeassistant.setup import async_setup_component


class TestHomeAssistantIntegration:
    """Test cases for Home Assistant integration."""

    @pytest.mark.asyncio
    async def test_setup_integration(self, hass: HomeAssistant):
        """Test integration setup."""
        config = {
            "marspro": {
                "username": "test@example.com",
                "password": "password123",
                "devices": [
                    {
                        "name": "Test Light",
                        "mac_address": "AA:BB:CC:DD:EE:FF",
                        "device_type": "light"
                    }
                ]
            }
        }
        
        with patch('src.marspro.api.MarsProAPI') as mock_api_class:
            mock_api = AsyncMock()
            mock_api_class.return_value = mock_api
            mock_api.authenticate.return_value = {"token": "test_token"}
            mock_api.get_devices.return_value = {"devices": [{"id": "1"}]}
            
            result = await async_setup_component(hass, "marspro", config)
            
            assert result is True
            mock_api.authenticate.assert_called_once()

    @pytest.mark.asyncio
    async def test_light_entity_creation(self, hass: HomeAssistant):
        """Test light entity creation."""
        config = {
            "marspro": {
                "username": "test@example.com",
                "password": "password123",
                "devices": [
                    {
                        "name": "Test Light",
                        "mac_address": "AA:BB:CC:DD:EE:FF",
                        "device_type": "light"
                    }
                ]
            }
        }
        
        with patch('src.marspro.api.MarsProAPI') as mock_api_class:
            mock_api = AsyncMock()
            mock_api_class.return_value = mock_api
            mock_api.authenticate.return_value = {"token": "test_token"}
            mock_api.get_devices.return_value = {"devices": [{"id": "1"}]}
            
            await async_setup_component(hass, "marspro", config)
            await hass.async_block_till_done()
            
            # Check if light entity was created
            light_entity = hass.states.get("light.test_light")
            assert light_entity is not None

    @pytest.mark.asyncio
    async def test_light_control(self, hass: HomeAssistant):
        """Test light control functionality."""
        config = {
            "marspro": {
                "username": "test@example.com",
                "password": "password123",
                "devices": [
                    {
                        "name": "Test Light",
                        "mac_address": "AA:BB:CC:DD:EE:FF",
                        "device_type": "light"
                    }
                ]
            }
        }
        
        with patch('src.marspro.api.MarsProAPI') as mock_api_class:
            mock_api = AsyncMock()
            mock_api_class.return_value = mock_api
            mock_api.authenticate.return_value = {"token": "test_token"}
            mock_api.get_devices.return_value = {"devices": [{"id": "1"}]}
            mock_api.control_device.return_value = {"status": "success"}
            
            await async_setup_component(hass, "marspro", config)
            await hass.async_block_till_done()
            
            # Test turning on the light
            await hass.services.async_call(
                "light", "turn_on", {"entity_id": "light.test_light"}
            )
            await hass.async_block_till_done()
            
            mock_api.control_device.assert_called() 