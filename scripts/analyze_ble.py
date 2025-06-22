#!/usr/bin/env python3
"""BLE Protocol Analysis Script."""

import subprocess
import sys
import time
from pathlib import Path

def start_ble_analysis():
    """Start BLE analysis with Frida."""
    print("Starting BLE protocol analysis...")
    
    # Start Frida with BLE hooks
    cmd = [
        "frida", "-U", "-f", "com.marspro.meizhi",
        "-l", "scripts/frida/ble_hook.js",
        "--no-pause"
    ]
    
    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print("\nBLE analysis stopped by user")
    except Exception as e:
        print(f"Error during BLE analysis: {e}")

if __name__ == "__main__":
    start_ble_analysis()
