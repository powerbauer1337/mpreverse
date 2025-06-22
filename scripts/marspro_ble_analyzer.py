#!/usr/bin/env python3
"""
MarsPro BLE Protocol Analyzer

This script helps analyze BLE communication between the MarsPro app and device.
It can scan for devices, connect to them, and log all BLE traffic for protocol analysis.

Note: This runs as a BLE client (central) on Windows, not as a peripheral.
For full emulation, use nRF Connect on Android or WSL2 with BlueZ.
"""

import asyncio
import logging
import json
import time
from datetime import datetime
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, asdict
from pathlib import Path

try:
    from bleak import BleakClient, BleakScanner
    from bleak.exc import BleakError
    from bleak.backends.device import BLEDevice
    from bleak.backends.scanner import AdvertisementData
    BLEAK_AVAILABLE = True
except ImportError:
    print("Error: bleak library not found. Install with: pip install bleak")
    BLEAK_AVAILABLE = False

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('analysis/ble_analysis.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


@dataclass
class BLETrafficLog:
    """BLE traffic log entry."""
    timestamp: str
    device_address: str
    operation: str  # 'read', 'write', 'notify'
    characteristic_uuid: str
    service_uuid: str
    data: str  # hex string
    direction: str  # 'in' or 'out'


@dataclass
class MarsProDevice:
    """MarsPro device information."""
    address: str
    name: str
    rssi: int
    services: List[str]
    manufacturer_data: Optional[str] = None  # Store as hex string


class MarsProBLEAnalyzer:
    """MarsPro BLE protocol analyzer."""
    
    def __init__(self):
        """Initialize the analyzer."""
        if not BLEAK_AVAILABLE:
            raise ImportError("bleak library is required")
        
        self.discovered_devices: Dict[str, MarsProDevice] = {}
        self.traffic_logs: List[BLETrafficLog] = []
        self.analysis_dir = Path("analysis")
        self.analysis_dir.mkdir(exist_ok=True)
        
        # MarsPro expected UUIDs (from static analysis)
        self.marspro_service_uuid = "0000ffe0-0000-1000-8000-00805f9b34fb"
        self.marspro_characteristics = [
            "0000ffe1-0000-1000-8000-00805f9b34fb",  # Command
            "0000ffe2-0000-1000-8000-00805f9b34fb",  # Data
            "0000ffe3-0000-1000-8000-00805f9b34fb",  # Config
            "0000ffe4-0000-1000-8000-00805f9b34fb",  # Status
        ]
    
    def log_traffic(self, device_address: str, operation: str, 
                   characteristic_uuid: str, service_uuid: str, 
                   data: Union[bytes, bytearray], direction: str):
        """Log BLE traffic for analysis."""
        # Convert bytearray to bytes if needed
        if isinstance(data, bytearray):
            data = bytes(data)
        
        log_entry = BLETrafficLog(
            timestamp=datetime.now().isoformat(),
            device_address=device_address,
            operation=operation,
            characteristic_uuid=characteristic_uuid,
            service_uuid=service_uuid,
            data=data.hex(),
            direction=direction
        )
        self.traffic_logs.append(log_entry)
        logger.info(f"BLE Traffic: {direction.upper()} {operation} on {characteristic_uuid} = {data.hex()}")
    
    def is_marspro_device(self, device: BLEDevice, advertisement_data: AdvertisementData) -> bool:
        """Check if a device might be a MarsPro device."""
        # Check device name
        if device.name and "marspro" in device.name.lower():
            return True
        
        # Check for MarsPro service UUID in advertisement
        if advertisement_data.service_uuids:
            for uuid in advertisement_data.service_uuids:
                if self.marspro_service_uuid.lower() in uuid.lower():
                    return True
        
        # Check manufacturer data for MarsPro patterns
        if advertisement_data.manufacturer_data:
            # Convert manufacturer data to hex string for logging
            if isinstance(advertisement_data.manufacturer_data, dict):
                # Handle dict format
                for company_id, data in advertisement_data.manufacturer_data.items():
                    logger.info(f"Manufacturer data for {device.address} (company {company_id}): {data.hex()}")
            else:
                # Handle bytes format
                logger.info(f"Manufacturer data for {device.address}: {advertisement_data.manufacturer_data.hex()}")
        
        return False
    
    async def scan_for_devices(self, timeout: float = 10.0) -> List[MarsProDevice]:
        """Scan for BLE devices and identify potential MarsPro devices."""
        logger.info(f"Scanning for BLE devices for {timeout} seconds...")
        
        def detection_callback(device: BLEDevice, advertisement_data: AdvertisementData):
            """Callback for device detection."""
            if self.is_marspro_device(device, advertisement_data):
                # Handle manufacturer data conversion
                manufacturer_data_str = None
                if advertisement_data.manufacturer_data:
                    if isinstance(advertisement_data.manufacturer_data, dict):
                        # Convert dict to hex string
                        for company_id, data in advertisement_data.manufacturer_data.items():
                            manufacturer_data_str = f"{company_id}:{data.hex()}"
                            break
                    else:
                        manufacturer_data_str = advertisement_data.manufacturer_data.hex()
                
                marspro_device = MarsProDevice(
                    address=device.address,
                    name=device.name or "Unknown",
                    rssi=advertisement_data.rssi,
                    services=list(advertisement_data.service_uuids) if advertisement_data.service_uuids else [],
                    manufacturer_data=manufacturer_data_str
                )
                self.discovered_devices[device.address] = marspro_device
                logger.info(f"Potential MarsPro device found: {device.name} ({device.address})")
        
        # Start scanning
        scanner = BleakScanner(detection_callback)
        await scanner.start()
        await asyncio.sleep(timeout)
        await scanner.stop()
        
        logger.info(f"Scan complete. Found {len(self.discovered_devices)} potential MarsPro devices")
        return list(self.discovered_devices.values())
    
    async def connect_and_analyze(self, device_address: str) -> bool:
        """Connect to a device and analyze its BLE communication."""
        logger.info(f"Connecting to device {device_address}...")
        
        try:
            async with BleakClient(device_address) as client:
                logger.info(f"Connected to {device_address}")
                
                # Discover services
                services = await client.get_services()
                logger.info(f"Discovered {len(list(services))} services")
                
                # Log all services and characteristics
                for service in services:
                    logger.info(f"Service: {service.uuid}")
                    for char in service.characteristics:
                        logger.info(f"  Characteristic: {char.uuid} - Properties: {char.properties}")
                        
                        # Try to read characteristics that support reading
                        if "read" in char.properties:
                            try:
                                data = await client.read_gatt_char(char.uuid)
                                self.log_traffic(
                                    device_address, "read", char.uuid, service.uuid, data, "in"
                                )
                            except Exception as e:
                                logger.warning(f"Failed to read {char.uuid}: {e}")
                
                # Enable notifications for characteristics that support them
                for service in services:
                    for char in service.characteristics:
                        if "notify" in char.properties:
                            try:
                                await client.start_notify(char.uuid, self.notification_handler)
                                logger.info(f"Enabled notifications for {char.uuid}")
                            except Exception as e:
                                logger.warning(f"Failed to enable notifications for {char.uuid}: {e}")
                
                # Keep connection alive for a while to capture traffic
                logger.info("Monitoring BLE traffic for 30 seconds...")
                await asyncio.sleep(30)
                
                return True
                
        except Exception as e:
            logger.error(f"Failed to connect to {device_address}: {e}")
            return False
    
    def notification_handler(self, sender, data):
        """Handle BLE notifications."""
        logger.info(f"Notification from {sender}: {data.hex()}")
        # Note: sender is the characteristic UUID
        self.log_traffic("unknown", "notify", str(sender), "unknown", data, "in")
    
    def save_analysis_results(self):
        """Save analysis results to files."""
        # Save discovered devices
        devices_file = self.analysis_dir / "discovered_devices.json"
        with open(devices_file, 'w') as f:
            json.dump([asdict(device) for device in self.discovered_devices.values()], f, indent=2)
        
        # Save traffic logs
        traffic_file = self.analysis_dir / "ble_traffic_logs.json"
        with open(traffic_file, 'w') as f:
            json.dump([asdict(log) for log in self.traffic_logs], f, indent=2)
        
        # Generate analysis report
        report_file = self.analysis_dir / "ble_analysis_report.md"
        with open(report_file, 'w') as f:
            f.write("# MarsPro BLE Analysis Report\n\n")
            f.write(f"Generated: {datetime.now().isoformat()}\n\n")
            
            f.write("## Discovered Devices\n\n")
            for device in self.discovered_devices.values():
                f.write(f"- **{device.name}** ({device.address})\n")
                f.write(f"  - RSSI: {device.rssi}\n")
                f.write(f"  - Services: {device.services}\n")
                if device.manufacturer_data:
                    f.write(f"  - Manufacturer Data: {device.manufacturer_data}\n")
                f.write("\n")
            
            f.write("## BLE Traffic Analysis\n\n")
            f.write(f"Total traffic entries: {len(self.traffic_logs)}\n\n")
            
            # Group by characteristic
            char_traffic = {}
            for log in self.traffic_logs:
                if log.characteristic_uuid not in char_traffic:
                    char_traffic[log.characteristic_uuid] = []
                char_traffic[log.characteristic_uuid].append(log)
            
            for char_uuid, logs in char_traffic.items():
                f.write(f"### Characteristic: {char_uuid}\n\n")
                for log in logs:
                    f.write(f"- **{log.timestamp}** {log.operation.upper()} {log.direction.upper()}: {log.data}\n")
                f.write("\n")
        
        logger.info(f"Analysis results saved to {self.analysis_dir}")
    
    async def run_analysis(self):
        """Run the complete BLE analysis."""
        logger.info("Starting MarsPro BLE protocol analysis...")
        
        # Scan for devices
        devices = await self.scan_for_devices()
        
        if not devices:
            logger.warning("No potential MarsPro devices found")
            return
        
        # Try to connect to each device
        for device in devices:
            logger.info(f"Attempting to connect to {device.name} ({device.address})")
            success = await self.connect_and_analyze(device.address)
            if success:
                logger.info(f"Successfully analyzed {device.name}")
                break
        
        # Save results
        self.save_analysis_results()
        logger.info("BLE analysis complete!")


async def main():
    """Main entry point."""
    try:
        analyzer = MarsProBLEAnalyzer()
        await analyzer.run_analysis()
    except KeyboardInterrupt:
        logger.info("Analysis interrupted by user")
    except Exception as e:
        logger.error(f"Analysis failed: {e}")


if __name__ == "__main__":
    asyncio.run(main()) 