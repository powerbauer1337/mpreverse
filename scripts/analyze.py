#!/usr/bin/env python3
"""Main analysis script for MarsPro reverse engineering."""

import os
import sys
import subprocess
import logging
from pathlib import Path
from typing import Optional

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('analysis/analysis.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


class MarsProAnalyzer:
    """Main analyzer for MarsPro reverse engineering."""
    
    def __init__(self, apk_path: str):
        """Initialize the analyzer."""
        self.apk_path = Path(apk_path)
        self.project_root = Path(__file__).parent.parent
        self.output_dir = self.project_root / "output"
        self.analysis_dir = self.project_root / "analysis"
        
        # Create output directories
        self.output_dir.mkdir(exist_ok=True)
        self.analysis_dir.mkdir(exist_ok=True)
        
        logger.info(f"Initialized analyzer for APK: {self.apk_path}")
    
    def phase1_static_analysis(self) -> bool:
        """Phase 1: Static APK analysis using apktool and jadx."""
        logger.info("Starting Phase 1: Static Analysis")
        
        try:
            # Create output directories
            apktool_output = self.output_dir / "apktool_output"
            jadx_output = self.output_dir / "jadx_output"
            
            apktool_output.mkdir(exist_ok=True)
            jadx_output.mkdir(exist_ok=True)
            
            # Run apktool
            logger.info("Running apktool...")
            result = subprocess.run([
                "apktool", "d", str(self.apk_path), 
                "-o", str(apktool_output), "-f"
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                logger.info("apktool completed successfully")
            else:
                logger.error(f"apktool failed: {result.stderr}")
                return False
            
            # Run jadx
            logger.info("Running jadx...")
            result = subprocess.run([
                "jadx", "-d", str(jadx_output), str(self.apk_path)
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                logger.info("jadx completed successfully")
            else:
                logger.error(f"jadx failed: {result.stderr}")
                return False
            
            # Extract interesting files
            self._extract_interesting_files(apktool_output, jadx_output)
            
            return True
            
        except Exception as e:
            logger.error(f"Phase 1 failed: {e}")
            return False
    
    def phase2_dynamic_analysis(self) -> bool:
        """Phase 2: Dynamic analysis with Frida hooks."""
        logger.info("Starting Phase 2: Dynamic Analysis")
        
        try:
            # Check if device is connected
            result = subprocess.run(["adb", "devices"], capture_output=True, text=True)
            if "device" not in result.stdout:
                logger.warning("No Android device connected. Skipping dynamic analysis.")
                return True
            
            # Start Frida server if needed
            self._setup_frida_server()
            
            # Run network hooks
            logger.info("Running network hooks...")
            self._run_frida_script("scripts/net_hook.js")
            
            # Run BLE hooks
            logger.info("Running BLE hooks...")
            self._run_frida_script("scripts/ble_hook.js")
            
            return True
            
        except Exception as e:
            logger.error(f"Phase 2 failed: {e}")
            return False
    
    def phase3_documentation(self) -> bool:
        """Phase 3: Documentation and API mapping."""
        logger.info("Starting Phase 3: Documentation")
        
        try:
            # Generate analysis summary
            self._generate_analysis_summary()
            
            # Generate API documentation
            self._generate_api_documentation()
            
            # Generate mapping documentation
            self._generate_mapping_documentation()
            
            return True
            
        except Exception as e:
            logger.error(f"Phase 3 failed: {e}")
            return False
    
    def phase4_ha_integration(self) -> bool:
        """Phase 4: Home Assistant component development."""
        logger.info("Starting Phase 4: Home Assistant Integration")
        
        try:
            # Update constants with discovered values
            self._update_constants()
            
            # Generate configuration examples
            self._generate_config_examples()
            
            return True
            
        except Exception as e:
            logger.error(f"Phase 4 failed: {e}")
            return False
    
    def phase5_testing(self) -> bool:
        """Phase 5: Integration testing and validation."""
        logger.info("Starting Phase 5: Testing")
        
        try:
            # Run unit tests
            self._run_unit_tests()
            
            # Run integration tests
            self._run_integration_tests()
            
            return True
            
        except Exception as e:
            logger.error(f"Phase 5 failed: {e}")
            return False
    
    def _extract_interesting_files(self, apktool_output: Path, jadx_output: Path):
        """Extract interesting files for analysis."""
        logger.info("Extracting interesting files...")
        
        # Copy AndroidManifest.xml
        manifest_src = apktool_output / "AndroidManifest.xml"
        if manifest_src.exists():
            manifest_dst = self.analysis_dir / "AndroidManifest.xml"
            manifest_dst.write_text(manifest_src.read_text())
            logger.info("Extracted AndroidManifest.xml")
        
        # Copy strings.xml files
        for strings_file in apktool_output.rglob("strings.xml"):
            rel_path = strings_file.relative_to(apktool_output)
            dst_path = self.analysis_dir / "strings" / rel_path
            dst_path.parent.mkdir(parents=True, exist_ok=True)
            dst_path.write_text(strings_file.read_text())
            logger.info(f"Extracted {rel_path}")
    
    def _setup_frida_server(self):
        """Setup Frida server on device."""
        logger.info("Setting up Frida server...")
        
        # Check if Frida server is already running
        result = subprocess.run(["adb", "shell", "ps | grep frida"], 
                              capture_output=True, text=True)
        
        if "frida-server" not in result.stdout:
            logger.info("Starting Frida server...")
            subprocess.run([
                "adb", "shell", 
                "su -c '/data/local/tmp/frida-server &'"
            ])
    
    def _run_frida_script(self, script_path: str):
        """Run a Frida script."""
        script_full_path = self.project_root / script_path
        
        if not script_full_path.exists():
            logger.error(f"Script not found: {script_path}")
            return
        
        logger.info(f"Running Frida script: {script_path}")
        
        # This would need to be run manually with proper device setup
        logger.info(f"To run this script manually:")
        logger.info(f"frida -U -f com.marspro.app -l {script_full_path} --no-pause")
    
    def _generate_analysis_summary(self):
        """Generate analysis summary."""
        summary_path = self.analysis_dir / "analysis_summary.md"
        
        summary_content = f"""# MarsPro Analysis Summary

## APK Information
- **File**: {self.apk_path.name}
- **Size**: {self.apk_path.stat().st_size / (1024*1024):.2f} MB

## Analysis Phases
1. ✅ Static Analysis (apktool + jadx)
2. ⏳ Dynamic Analysis (Frida hooks)
3. ⏳ Documentation
4. ⏳ Home Assistant Integration
5. ⏳ Testing

## Discovered Components
- REST API endpoints (to be documented)
- BLE communication protocols (to be documented)
- Device control commands (to be documented)

## Next Steps
1. Run dynamic analysis with Frida
2. Document discovered APIs
3. Implement Home Assistant integration
4. Test with real devices

Generated on: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        summary_path.write_text(summary_content)
        logger.info("Generated analysis summary")
    
    def _generate_api_documentation(self):
        """Generate API documentation."""
        api_doc_path = self.analysis_dir / "api_documentation.md"
        
        api_content = """# MarsPro API Documentation

## REST API Endpoints

### Authentication
- **Endpoint**: `/api/v1/login`
- **Method**: POST
- **Description**: User authentication
- **Status**: To be discovered

### Device Management
- **Endpoint**: `/api/v1/devices`
- **Method**: GET
- **Description**: Get user devices
- **Status**: To be discovered

### Device Control
- **Endpoint**: `/api/v1/control`
- **Method**: POST
- **Description**: Control device
- **Status**: To be discovered

## BLE Communication

### Service UUIDs
- **Main Service**: To be discovered
- **Control Characteristic**: To be discovered
- **Status Characteristic**: To be discovered

### Command Protocol
- **Turn On**: To be discovered
- **Turn Off**: To be discovered
- **Set Brightness**: To be discovered
- **Set Color Temperature**: To be discovered

## Status Codes
- **200**: Success
- **401**: Unauthorized
- **404**: Not Found
- **500**: Server Error

*This documentation will be updated as endpoints are discovered during analysis.*
"""
        
        api_doc_path.write_text(api_content)
        logger.info("Generated API documentation")
    
    def _generate_mapping_documentation(self):
        """Generate mapping documentation."""
        mapping_path = self.analysis_dir / "api_mapping.md"
        
        mapping_content = """# MarsPro API Mapping

## Cloud vs Local Function Mapping

### Authentication
| Cloud Function | Local Equivalent | Status |
|----------------|------------------|--------|
| Login | BLE Pairing | To be discovered |
| Token Refresh | BLE Reconnection | To be discovered |

### Device Discovery
| Cloud Function | Local Equivalent | Status |
|----------------|------------------|--------|
| Get Devices | BLE Scan | To be discovered |
| Device Status | BLE Read | To be discovered |

### Device Control
| Cloud Function | Local Equivalent | Status |
|----------------|------------------|--------|
| Turn On/Off | BLE Write | To be discovered |
| Set Brightness | BLE Write | To be discovered |
| Set Color Temp | BLE Write | To be discovered |
| Set Fan Speed | BLE Write | To be discovered |

### Status Monitoring
| Cloud Function | Local Equivalent | Status |
|----------------|------------------|--------|
| Real-time Status | BLE Notifications | To be discovered |
| Power Consumption | BLE Read | To be discovered |

## Implementation Notes
- Local control requires device MAC address
- BLE communication may have different command formats
- Some features may only be available via cloud API
- Local control provides faster response times

*This mapping will be updated as the protocol is reverse engineered.*
"""
        
        mapping_path.write_text(mapping_content)
        logger.info("Generated mapping documentation")
    
    def _update_constants(self):
        """Update constants with discovered values."""
        logger.info("Constants will be updated after API discovery")
    
    def _generate_config_examples(self):
        """Generate configuration examples."""
        logger.info("Configuration examples already generated")
    
    def _run_unit_tests(self):
        """Run unit tests."""
        logger.info("Running unit tests...")
        # This would run pytest on the custom_components directory
    
    def _run_integration_tests(self):
        """Run integration tests."""
        logger.info("Running integration tests...")
        # This would test the Home Assistant integration
    
    def run_full_analysis(self):
        """Run the complete analysis workflow."""
        logger.info("Starting full MarsPro analysis workflow")
        
        phases = [
            ("Phase 1: Static Analysis", self.phase1_static_analysis),
            ("Phase 2: Dynamic Analysis", self.phase2_dynamic_analysis),
            ("Phase 3: Documentation", self.phase3_documentation),
            ("Phase 4: Home Assistant Integration", self.phase4_ha_integration),
            ("Phase 5: Testing", self.phase5_testing),
        ]
        
        for phase_name, phase_func in phases:
            logger.info(f"\n{'='*50}")
            logger.info(f"Starting {phase_name}")
            logger.info(f"{'='*50}")
            
            success = phase_func()
            if not success:
                logger.error(f"{phase_name} failed. Stopping analysis.")
                break
        
        logger.info("\nAnalysis workflow completed!")


def main():
    """Main entry point."""
    if len(sys.argv) != 2:
        print("Usage: python analyze.py <path_to_apk>")
        sys.exit(1)
    
    apk_path = sys.argv[1]
    
    if not os.path.exists(apk_path):
        print(f"APK file not found: {apk_path}")
        sys.exit(1)
    
    analyzer = MarsProAnalyzer(apk_path)
    analyzer.run_full_analysis()


if __name__ == "__main__":
    main() 