#!/usr/bin/env python3
"""Network Protocol Analysis Script."""

import subprocess
import sys
import time
from pathlib import Path

def start_network_analysis():
    """Start network analysis with Frida."""
    print("Starting network protocol analysis...")
    
    # Start Frida with network hooks
    cmd = [
        "frida", "-U", "-f", "com.marspro.meizhi",
        "-l", "scripts/frida/net_hook.js",
        "--no-pause"
    ]
    
    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print("\nNetwork analysis stopped by user")
    except Exception as e:
        print(f"Error during network analysis: {e}")

if __name__ == "__main__":
    start_network_analysis()
