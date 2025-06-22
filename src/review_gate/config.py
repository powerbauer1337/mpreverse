"""
Review Gate V2 Configuration

Configuration settings for the Review Gate V2 MCP server.
"""

import os
from pathlib import Path

# Server configuration
SERVER_NAME = "review-gate-v2"
SERVER_VERSION = "2.0.0"
SERVER_DESCRIPTION = "Review Gate V2 MCP Server for interactive development reviews"

# File paths
ASSETS_DIR = Path(__file__).parent.parent.parent / "assets" / "review_gate"
CURSOR_EXTENSION_DIR = ASSETS_DIR / "cursor-extension"
INSTALLERS_DIR = ASSETS_DIR / "installers"

# MCP server settings
DEFAULT_TIMEOUT = 300  # 5 minutes
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
SUPPORTED_IMAGE_FORMATS = [".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp"]

# UI settings
POPUP_TITLE = "Review Gate V2 - Final Review"
DEFAULT_MESSAGE = "Please review the work and provide feedback or type 'TASK_COMPLETE' when satisfied."

# Speech-to-text settings
WHISPER_MODEL = "base"
WHISPER_DEVICE = "cpu"
WHISPER_COMPUTE_TYPE = "int8"

# Environment variables
DEBUG_MODE = os.getenv("REVIEW_GATE_DEBUG", "false").lower() == "true"
LOG_LEVEL = os.getenv("REVIEW_GATE_LOG_LEVEL", "INFO") 