"""
Unit tests for MarsPro API client.
"""

import pytest
from unittest.mock import AsyncMock, patch
from src.marspro.api import MarsProAPI


class TestMarsProAPI:
    """Test cases for MarsProAPI class."""

    @pytest.fixture
    def api_client(self):
        """Create a MarsProAPI instance for testing."""
        return MarsProAPI("test@example.com", "password123")

    @pytest.mark.asyncio
    async def test_initialization(self, api_client):
        """Test API client initialization."""
        assert api_client.username == "test@example.com"
        assert api_client.password == "password123"
        assert api_client.base_url == "https://api.marspro.com"

    @pytest.mark.asyncio
    async def test_authentication(self, api_client):
        """Test authentication flow."""
        with patch.object(api_client, '_make_request') as mock_request:
            mock_request.return_value = {"token": "test_token"}
            
            result = await api_client.authenticate()
            
            assert result == {"token": "test_token"}
            mock_request.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_devices(self, api_client):
        """Test device retrieval."""
        with patch.object(api_client, '_make_request') as mock_request:
            mock_request.return_value = {"devices": [{"id": "1", "name": "Test Device"}]}
            
            result = await api_client.get_devices()
            
            assert result == {"devices": [{"id": "1", "name": "Test Device"}]}
            mock_request.assert_called_once()

    @pytest.mark.asyncio
    async def test_control_device(self, api_client):
        """Test device control."""
        with patch.object(api_client, '_make_request') as mock_request:
            mock_request.return_value = {"status": "success"}
            
            result = await api_client.control_device("device_id", "turn_on")
            
            assert result == {"status": "success"}
            mock_request.assert_called_once()

    @pytest.mark.asyncio
    async def test_ble_connection(self, api_client):
        """Test BLE connection."""
        with patch('bleak.BleakClient') as mock_bleak:
            mock_client = AsyncMock()
            mock_bleak.return_value = mock_client
            
            await api_client.connect_ble("AA:BB:CC:DD:EE:FF")
            
            mock_bleak.assert_called_once_with("AA:BB:CC:DD:EE:FF")
            mock_client.connect.assert_called_once() 