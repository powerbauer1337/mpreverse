"""
Unit tests for MarsPro coordinator.
"""

import pytest
from unittest.mock import AsyncMock, patch
from src.marspro.coordinator import MarsProCoordinator


class TestMarsProCoordinator:
    """Test cases for MarsProCoordinator class."""

    @pytest.fixture
    def coordinator(self):
        """Create a MarsProCoordinator instance for testing."""
        return MarsProCoordinator("test@example.com", "password123")

    @pytest.mark.asyncio
    async def test_initialization(self, coordinator):
        """Test coordinator initialization."""
        assert coordinator.username == "test@example.com"
        assert coordinator.password == "password123"

    @pytest.mark.asyncio
    async def test_start(self, coordinator):
        """Test coordinator start."""
        with patch.object(coordinator, 'api') as mock_api:
            mock_api.authenticate.return_value = {"token": "test_token"}
            
            await coordinator.start()
            
            mock_api.authenticate.assert_called_once()

    @pytest.mark.asyncio
    async def test_stop(self, coordinator):
        """Test coordinator stop."""
        with patch.object(coordinator, 'api') as mock_api:
            await coordinator.stop()
            
            mock_api.disconnect.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_devices(self, coordinator):
        """Test device retrieval."""
        with patch.object(coordinator, 'api') as mock_api:
            mock_api.get_devices.return_value = {"devices": [{"id": "1"}]}
            
            result = await coordinator.get_devices()
            
            assert result == {"devices": [{"id": "1"}]}
            mock_api.get_devices.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_device(self, coordinator):
        """Test device update."""
        with patch.object(coordinator, 'api') as mock_api:
            mock_api.control_device.return_value = {"status": "success"}
            
            result = await coordinator.update_device("device_id", {"state": "on"})
            
            assert result == {"status": "success"}
            mock_api.control_device.assert_called_once() 