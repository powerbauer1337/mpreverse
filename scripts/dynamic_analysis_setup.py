#!/usr/bin/env python3
"""Dynamic Analysis Setup Script for MarsPro Protocol Discovery."""

import os
import sys
import subprocess
import logging
from pathlib import Path
from typing import Optional, List

# Setup logging with UTF-8 encoding
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('analysis/dynamic_analysis.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


class DynamicAnalysisSetup:
    """Setup and manage dynamic analysis environment."""
    
    def __init__(self):
        """Initialize the dynamic analysis setup."""
        self.project_root = Path(__file__).parent.parent
        self.scripts_dir = self.project_root / "scripts"
        self.frida_dir = self.scripts_dir / "frida"
        self.analysis_dir = self.project_root / "analysis"
        self.output_dir = self.project_root / "output"
        self.tools_dir = self.project_root / "assets" / "tools"
        
        # Create directories
        self.analysis_dir.mkdir(exist_ok=True)
        self.output_dir.mkdir(exist_ok=True)
        
        logger.info("Initialized Dynamic Analysis Setup")
    
    def find_adb(self) -> Optional[Path]:
        """Find ADB executable in project tools or system PATH."""
        # Check project tools first
        adb_path = self.tools_dir / "android-platform-tools" / "adb.exe"
        if adb_path.exists():
            logger.info(f"Found ADB in project tools: {adb_path}")
            return adb_path
        
        # Check system PATH
        try:
            result = subprocess.run(["where", "adb"], capture_output=True, text=True)
            if result.returncode == 0:
                adb_path = Path(result.stdout.strip().split('\n')[0])
                logger.info(f"Found ADB in system PATH: {adb_path}")
                return adb_path
        except Exception:
            pass
        
        return None
    
    def check_prerequisites(self) -> bool:
        """Check if all prerequisites are met."""
        logger.info("Checking prerequisites...")
        
        # Check if ADB is available
        adb_path = self.find_adb()
        if adb_path:
            try:
                result = subprocess.run([str(adb_path), "version"], capture_output=True, text=True)
                if result.returncode == 0:
                    logger.info("ADB is available")
                    self.adb_path = adb_path
                else:
                    logger.error("ADB not found or not working")
                    return False
            except Exception as e:
                logger.error(f"Error checking ADB: {e}")
                return False
        else:
            logger.error("ADB not found in PATH or project tools")
            return False
        
        # Check if Frida is available
        try:
            result = subprocess.run(["frida", "--version"], capture_output=True, text=True)
            if result.returncode == 0:
                logger.info("Frida is available")
            else:
                logger.error("Frida not found or not working")
                return False
        except FileNotFoundError:
            logger.error("Frida not found in PATH")
            return False
        
        # Check if Frida scripts exist
        ble_script = self.frida_dir / "ble_hook.js"
        net_script = self.frida_dir / "net_hook.js"
        
        if ble_script.exists():
            logger.info("BLE hook script found")
        else:
            logger.error("BLE hook script not found")
            return False
        
        if net_script.exists():
            logger.info("Network hook script found")
        else:
            logger.error("Network hook script not found")
            return False
        
        return True
    
    def check_device_connection(self) -> bool:
        """Check if Android device is connected."""
        logger.info("Checking device connection...")
        
        try:
            result = subprocess.run([str(self.adb_path), "devices"], capture_output=True, text=True)
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')[1:]  # Skip header
                devices = [line for line in lines if line.strip() and 'device' in line]
                
                if devices:
                    logger.info(f"Found {len(devices)} connected device(s)")
                    for device in devices:
                        logger.info(f"  - {device}")
                    return True
                else:
                    logger.warning("No devices connected")
                    return False
            else:
                logger.error("Failed to check devices")
                return False
        except Exception as e:
            logger.error(f"Error checking devices: {e}")
            return False
    
    def check_frida_server(self) -> bool:
        """Check if Frida server is running on device."""
        logger.info("Checking Frida server...")
        
        try:
            result = subprocess.run(
                [str(self.adb_path), "shell", "ps | grep frida"], 
                capture_output=True, text=True
            )
            
            if "frida-server" in result.stdout:
                logger.info("Frida server is running")
                return True
            else:
                logger.warning("Frida server not running")
                return False
        except Exception as e:
            logger.error(f"Error checking Frida server: {e}")
            return False
    
    def install_frida_server(self) -> bool:
        """Install and start Frida server on device."""
        logger.info("Installing Frida server...")
        
        try:
            # Check if device is rooted
            result = subprocess.run(
                [str(self.adb_path), "shell", "su -c 'id'"], 
                capture_output=True, text=True
            )
            
            if result.returncode != 0:
                logger.error("Device is not rooted. Frida server requires root access.")
                return False
            
            # Download Frida server (this would need to be done manually)
            logger.info("Please download Frida server for your device architecture")
            logger.info("   Visit: https://github.com/frida/frida/releases")
            logger.info("   Download: frida-server-<version>-android-<arch>.xz")
            
            # Instructions for manual installation
            logger.info("Manual installation steps:")
            logger.info("   1. Extract the downloaded frida-server")
            logger.info("   2. Push to device: adb push frida-server /data/local/tmp/")
            logger.info("   3. Set permissions: adb shell chmod 755 /data/local/tmp/frida-server")
            logger.info("   4. Start server: adb shell su -c '/data/local/tmp/frida-server &'")
            
            return False  # Manual installation required
            
        except Exception as e:
            logger.error(f"Error installing Frida server: {e}")
            return False
    
    def setup_network_monitoring(self) -> bool:
        """Setup network monitoring tools."""
        logger.info("Setting up network monitoring...")
        
        try:
            # Create network monitoring directory
            network_dir = self.output_dir / "network_capture"
            network_dir.mkdir(exist_ok=True)
            
            # Create monitoring script for Windows
            monitor_script = network_dir / "start_monitoring.bat"
            with open(monitor_script, 'w') as f:
                f.write("""@echo off
REM Network monitoring script for MarsPro analysis

echo Starting network monitoring...

REM Start tcpdump on device
adb shell "su -c 'tcpdump -i any -w /sdcard/marspro_capture.pcap'"

echo Network monitoring started. Capture file: /sdcard/marspro_capture.pcap
echo To stop: adb shell "su -c \"pkill tcpdump\""
echo To download: adb pull /sdcard/marspro_capture.pcap .
""")
            
            logger.info("Network monitoring setup complete")
            logger.info(f"  Script: {monitor_script}")
            return True
            
        except Exception as e:
            logger.error(f"Error setting up network monitoring: {e}")
            return False
    
    def create_analysis_scripts(self) -> bool:
        """Create analysis scripts for protocol discovery."""
        logger.info("Creating analysis scripts...")
        
        try:
            # Create BLE analysis script
            ble_analysis = self.scripts_dir / "analyze_ble.py"
            with open(ble_analysis, 'w') as f:
                f.write("""#!/usr/bin/env python3
\"\"\"BLE Protocol Analysis Script.\"\"\"

import subprocess
import sys
import time
from pathlib import Path

def start_ble_analysis():
    \"\"\"Start BLE analysis with Frida.\"\"\"
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
        print("\\nBLE analysis stopped by user")
    except Exception as e:
        print(f"Error during BLE analysis: {e}")

if __name__ == "__main__":
    start_ble_analysis()
""")
            
            # Create network analysis script
            net_analysis = self.scripts_dir / "analyze_network.py"
            with open(net_analysis, 'w') as f:
                f.write("""#!/usr/bin/env python3
\"\"\"Network Protocol Analysis Script.\"\"\"

import subprocess
import sys
import time
from pathlib import Path

def start_network_analysis():
    \"\"\"Start network analysis with Frida.\"\"\"
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
        print("\\nNetwork analysis stopped by user")
    except Exception as e:
        print(f"Error during network analysis: {e}")

if __name__ == "__main__":
    start_network_analysis()
""")
            
            logger.info("Analysis scripts created")
            logger.info(f"  BLE analysis: {ble_analysis}")
            logger.info(f"  Network analysis: {net_analysis}")
            return True
            
        except Exception as e:
            logger.error(f"Error creating analysis scripts: {e}")
            return False
    
    def create_protocol_documentation_template(self) -> bool:
        """Create template for protocol documentation."""
        logger.info("Creating protocol documentation template...")
        
        try:
            protocol_doc = self.analysis_dir / "protocol_discovery_template.md"
            with open(protocol_doc, 'w', encoding='utf-8') as f:
                f.write("""# MarsPro Protocol Discovery Template

## BLE Communication Protocol

### Service UUIDs
- **Primary Service**: `[TO BE DISCOVERED]`
- **Secondary Service**: `[TO BE DISCOVERED]`

### Characteristic UUIDs
- **Command Characteristic**: `[TO BE DISCOVERED]`
- **Data Characteristic**: `[TO BE DISCOVERED]`
- **Status Characteristic**: `[TO BE DISCOVERED]`
- **Configuration Characteristic**: `[TO BE DISCOVERED]`

### Command Format
```
[TO BE DISCOVERED]
```

### Data Format
```
[TO BE DISCOVERED]
```

## Network API Protocol

### Base URLs
- **Primary API**: `[TO BE DISCOVERED]`
- **Firebase**: `[TO BE DISCOVERED]`

### Authentication
- **Method**: `[TO BE DISCOVERED]`
- **Token Format**: `[TO BE DISCOVERED]`

### Endpoints
- **Login**: `[TO BE DISCOVERED]`
- **Device List**: `[TO BE DISCOVERED]`
- **Device Control**: `[TO BE DISCOVERED]`
- **Device Status**: `[TO BE DISCOVERED]`

### Request/Response Format
```
[TO BE DISCOVERED]
```

## Discovery Log

### Session Information
- **Date**: [DATE]
- **Device**: [DEVICE MODEL]
- **App Version**: [VERSION]
- **Analysis Tool**: Frida

### BLE Discoveries
- [ ] Service UUIDs identified
- [ ] Characteristic UUIDs identified
- [ ] Command format understood
- [ ] Data format understood
- [ ] Authentication mechanism identified

### Network Discoveries
- [ ] API endpoints identified
- [ ] Authentication flow understood
- [ ] Request/response format documented
- [ ] Error handling patterns identified

### Notes
[Add any additional observations or patterns discovered during analysis]

## Next Steps
1. Update BLE client with discovered UUIDs
2. Implement actual protocol parsing
3. Test with real devices
4. Complete Home Assistant integration
""")
            
            logger.info("Protocol documentation template created")
            logger.info(f"  Template: {protocol_doc}")
            return True
            
        except Exception as e:
            logger.error(f"Error creating protocol template: {e}")
            return False
    
    def run_setup(self) -> bool:
        """Run complete setup process."""
        logger.info("Starting Dynamic Analysis Setup")
        logger.info("=" * 50)
        
        # Check prerequisites
        if not self.check_prerequisites():
            logger.error("Prerequisites check failed")
            return False
        
        # Check device connection
        if not self.check_device_connection():
            logger.warning("No device connected. Setup will continue but analysis requires a device.")
        
        # Check Frida server
        if not self.check_frida_server():
            logger.warning("Frida server not running. Manual installation required.")
            self.install_frida_server()
        
        # Setup network monitoring
        if not self.setup_network_monitoring():
            logger.error("Network monitoring setup failed")
            return False
        
        # Create analysis scripts
        if not self.create_analysis_scripts():
            logger.error("Analysis script creation failed")
            return False
        
        # Create protocol documentation template
        if not self.create_protocol_documentation_template():
            logger.error("Protocol template creation failed")
            return False
        
        logger.info("=" * 50)
        logger.info("Dynamic Analysis Setup Complete!")
        logger.info("")
        logger.info("Next Steps:")
        logger.info("1. Connect a rooted Android device")
        logger.info("2. Install and start Frida server")
        logger.info("3. Install MarsPro app on device")
        logger.info("4. Run analysis scripts:")
        logger.info("   - python scripts/analyze_ble.py")
        logger.info("   - python scripts/analyze_network.py")
        logger.info("5. Document discovered protocols")
        
        return True


def main():
    """Main setup function."""
    setup = DynamicAnalysisSetup()
    success = setup.run_setup()
    
    if success:
        print("\\nSetup completed successfully!")
        sys.exit(0)
    else:
        print("\\nSetup failed. Check logs for details.")
        sys.exit(1)


if __name__ == "__main__":
    main() 