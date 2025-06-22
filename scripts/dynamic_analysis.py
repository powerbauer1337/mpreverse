#!/usr/bin/env python3
"""
Dynamic analysis script for MarsPro reverse engineering
Uses Frida to hook BLE and network operations
"""

import os
import sys
import subprocess
import json
import time
import logging
from pathlib import Path
from typing import Dict, List, Optional

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('analysis/dynamic_analysis.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


class MarsProDynamicAnalyzer:
    """Dynamic analyzer for MarsPro using Frida."""
    
    def __init__(self):
        """Initialize the dynamic analyzer."""
        self.project_root = Path(__file__).parent.parent
        self.analysis_dir = self.project_root / "analysis"
        self.frida_scripts_dir = self.project_root / "scripts" / "frida"
        
        # Create analysis directory
        self.analysis_dir.mkdir(exist_ok=True)
        
        logger.info("Initialized MarsPro Dynamic Analyzer")
    
    def check_frida_installation(self) -> bool:
        """Check if Frida is properly installed."""
        try:
            result = subprocess.run(["frida", "--version"], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                logger.info(f"Frida version: {result.stdout.strip()}")
                return True
            else:
                logger.error("Frida not found or not working")
                return False
        except FileNotFoundError:
            logger.error("Frida not installed. Install with: pip install frida-tools")
            return False
    
    def check_device_connection(self) -> bool:
        """Check if Android device is connected."""
        try:
            result = subprocess.run(["adb", "devices"], 
                                  capture_output=True, text=True)
            if "device" in result.stdout and "List of devices" in result.stdout:
                devices = [line for line in result.stdout.split('\n') 
                          if '\tdevice' in line]
                if devices:
                    logger.info(f"Found {len(devices)} connected device(s)")
                    return True
                else:
                    logger.warning("No devices connected")
                    return False
            else:
                logger.error("ADB not working properly")
                return False
        except FileNotFoundError:
            logger.error("ADB not found. Install Android SDK Platform Tools")
            return False
    
    def create_ble_hook_script(self) -> Path:
        """Create an enhanced BLE hook script."""
        script_content = '''// Enhanced BLE Hook Script for MarsPro
// This script hooks Bluetooth operations to capture communication

console.log("[+] MarsPro Enhanced BLE Hook Loaded");

// Hook BluetoothGatt operations
try {
    var BluetoothGatt = Java.use("android.bluetooth.BluetoothGatt");
    
    BluetoothGatt.connect.implementation = function() {
        console.log("[BLE] connect() called");
        console.log("[BLE] Device: " + this.getDevice().getAddress());
        return this.connect();
    };
    
    BluetoothGatt.discoverServices.implementation = function() {
        console.log("[BLE] discoverServices() called");
        return this.discoverServices();
    };
    
    BluetoothGatt.readCharacteristic.implementation = function(characteristic) {
        console.log("[BLE] readCharacteristic() called");
        console.log("[BLE] Service UUID: " + characteristic.getService().getUuid());
        console.log("[BLE] Characteristic UUID: " + characteristic.getUuid());
        return this.readCharacteristic(characteristic);
    };
    
    BluetoothGatt.writeCharacteristic.implementation = function(characteristic) {
        console.log("[BLE] writeCharacteristic() called");
        console.log("[BLE] Service UUID: " + characteristic.getService().getUuid());
        console.log("[BLE] Characteristic UUID: " + characteristic.getUuid());
        console.log("[BLE] Value: " + characteristic.getValue());
        return this.writeCharacteristic(characteristic);
    };
    
    console.log("[+] BluetoothGatt hooks installed");
} catch (e) {
    console.log("[-] Failed to hook BluetoothGatt: " + e);
}

// Hook BluetoothGattCallback
try {
    var BluetoothGattCallback = Java.use("android.bluetooth.BluetoothGattCallback");
    
    BluetoothGattCallback.onServicesDiscovered.implementation = function(gatt, status) {
        console.log("[BLE] onServicesDiscovered() called");
        console.log("[BLE] Status: " + status);
        if (status === 0) { // GATT_SUCCESS
            var services = gatt.getServices();
            console.log("[BLE] Found " + services.size() + " services:");
            for (var i = 0; i < services.size(); i++) {
                var service = services.get(i);
                console.log("[BLE] Service: " + service.getUuid());
            }
        }
        return this.onServicesDiscovered(gatt, status);
    };
    
    console.log("[+] BluetoothGattCallback hooks installed");
} catch (e) {
    console.log("[-] Failed to hook BluetoothGattCallback: " + e);
}

console.log("[+] MarsPro BLE Hook Complete");
'''
        
        script_path = self.frida_scripts_dir / "enhanced_ble_hook.js"
        script_path.write_text(script_content)
        logger.info(f"Created enhanced BLE hook script: {script_path}")
        return script_path
    
    def create_network_hook_script(self) -> Path:
        """Create an enhanced network hook script."""
        script_content = '''// Enhanced Network Hook Script for MarsPro
// This script hooks network operations to capture API calls

console.log("[+] MarsPro Enhanced Network Hook Loaded");

// Hook OkHttp (commonly used in Android apps)
try {
    var OkHttpClient = Java.use("okhttp3.OkHttpClient");
    
    OkHttpClient.newCall.implementation = function(request) {
        console.log("[NET] HTTP Request:");
        console.log("[NET] URL: " + request.url().toString());
        console.log("[NET] Method: " + request.method());
        return this.newCall(request);
    };
    
    console.log("[+] OkHttp hooks installed");
} catch (e) {
    console.log("[-] OkHttp not found: " + e);
}

console.log("[+] MarsPro Network Hook Complete");
'''
        
        script_path = self.frida_scripts_dir / "enhanced_network_hook.js"
        script_path.write_text(script_content)
        logger.info(f"Created enhanced network hook script: {script_path}")
        return script_path
    
    def run_dynamic_analysis(self, package_name: str = "com.marspro.meizhi") -> bool:
        """Run dynamic analysis on the MarsPro app."""
        logger.info(f"Starting dynamic analysis on {package_name}")
        
        # Check prerequisites
        if not self.check_frida_installation():
            return False
        
        if not self.check_device_connection():
            return False
        
        # Create hook scripts
        ble_script = self.create_ble_hook_script()
        network_script = self.create_network_hook_script()
        
        logger.info("Dynamic analysis setup complete!")
        logger.info("To run the analysis:")
        logger.info(f"1. Install Frida server on your rooted device")
        logger.info(f"2. Run: frida -U -f {package_name} -l {ble_script} -l {network_script}")
        logger.info(f"3. Use the MarsPro app to trigger BLE and network operations")
        
        return True
    
    def generate_dynamic_report(self) -> None:
        """Generate a report from dynamic analysis findings."""
        report_content = f"""# MarsPro Dynamic Analysis Report

## Analysis Summary

This report contains findings from dynamic analysis of the MarsPro application using Frida hooks.

## Prerequisites

### Required Tools
- Frida (Python package)
- ADB (Android Debug Bridge)
- Rooted Android device (for Frida server)

### Setup Instructions
1. Install Frida: `pip install frida-tools`
2. Install Frida server on rooted device
3. Enable USB debugging on Android device
4. Connect device via USB

## Hook Scripts

### BLE Hook Script
- **File**: `scripts/frida/enhanced_ble_hook.js`
- **Purpose**: Capture Bluetooth Low Energy communication
- **Hooks**:
  - BluetoothGatt operations
  - BluetoothGattCallback events
  - Service discovery

### Network Hook Script
- **File**: `scripts/frida/enhanced_network_hook.js`
- **Purpose**: Capture network API calls
- **Hooks**:
  - OkHttp requests
  - HTTP communication

## Usage Instructions

1. **Start the analysis**:
   ```bash
   python scripts/dynamic_analysis.py
   ```

2. **Run Frida manually**:
   ```bash
   frida -U -f com.marspro.meizhi -l scripts/frida/enhanced_ble_hook.js -l scripts/frida/enhanced_network_hook.js
   ```

3. **Use the MarsPro app**:
   - Launch the app
   - Connect to a MarsPro device
   - Perform various operations
   - Monitor the console output

## Expected Findings

### BLE Communication
- Device discovery process
- Service discovery
- Characteristic reads/writes
- Notification subscriptions

### Network Communication
- Firebase authentication
- API endpoints
- Data synchronization
- Cloud storage operations

## Next Steps

1. **Document discovered protocols**
2. **Implement communication libraries**
3. **Create Home Assistant integration**
4. **Test with actual devices**

---

**Generated**: {time.strftime('%Y-%m-%d %H:%M:%S')}
**Version**: 1.0
"""
        
        report_path = self.analysis_dir / "dynamic_analysis_report.md"
        report_path.write_text(report_content)
        logger.info(f"Generated dynamic analysis report: {report_path}")


def main():
    """Main function for dynamic analysis."""
    print("🚀 MarsPro Dynamic Analysis")
    print("=" * 50)
    
    analyzer = MarsProDynamicAnalyzer()
    
    # Generate reports
    analyzer.generate_dynamic_report()
    
    # Run dynamic analysis
    success = analyzer.run_dynamic_analysis()
    
    if success:
        print("\n✅ Dynamic analysis setup completed successfully!")
        print("📋 Check the analysis/dynamic_analysis_report.md for details")
    else:
        print("\n❌ Dynamic analysis setup failed. Check the logs for details.")


if __name__ == "__main__":
    main() 