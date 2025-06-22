"""Constants for the MarsPro integration."""

from homeassistant.const import Platform

DOMAIN = "marspro"

# Configuration keys
CONF_EMAIL = "email"
CONF_PASSWORD = "password"
CONF_USE_CLOUD = "use_cloud"
CONF_BLE_MAC = "ble_mac"
CONF_SCAN_INTERVAL = "scan_interval"

# Platforms
PLATFORMS = [Platform.LIGHT, Platform.FAN, Platform.SENSOR]

# Default values
DEFAULT_SCAN_INTERVAL = 30
DEFAULT_TIMEOUT = 10
DEFAULT_RETRY_ATTEMPTS = 3

# BLE Service UUIDs (to be discovered)
# These are placeholder values based on common IoT patterns
BLE_SERVICE_UUID = "0000ffe0-0000-1000-8000-00805f9b34fb"
BLE_CHARACTERISTIC_UUID = "0000ffe1-0000-1000-8000-00805f9b34fb"

# API endpoints (to be discovered)
API_BASE_URL = "https://api.marspro.com"  # Placeholder
API_VERSION = "v1"  # Placeholder
API_LOGIN_ENDPOINT = "/api/v1/login"
API_DEVICES_ENDPOINT = "/api/v1/devices"
API_CONTROL_ENDPOINT = "/api/v1/control"

# Device types
DEVICE_TYPE_LIGHT = "light"
DEVICE_TYPE_FAN = "fan"
DEVICE_TYPE_SENSOR = "sensor"

# Command types
CMD_POWER_ON = "power_on"
CMD_POWER_OFF = "power_off"
CMD_SET_BRIGHTNESS = "set_brightness"
CMD_SET_COLOR = "set_color"
CMD_SET_FAN_SPEED = "set_fan_speed"
CMD_GET_STATUS = "get_status"

# Status values
STATUS_ON = "on"
STATUS_OFF = "off"
STATUS_UNKNOWN = "unknown"

# Error messages
ERROR_CONNECTION_FAILED = "Connection to MarsPro failed"
ERROR_AUTHENTICATION_FAILED = "Authentication failed"
ERROR_DEVICE_NOT_FOUND = "Device not found"
ERROR_COMMAND_FAILED = "Command failed"

# Logging
LOGGER_NAME = "custom_components.marspro" 