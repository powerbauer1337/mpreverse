#!/usr/bin/env python3
"""
Setup script for Android development tools
Downloads and configures ADB and other Android tools for MarsPro analysis
"""

import os
import sys
import subprocess
import urllib.request
import zipfile
import shutil
from pathlib import Path
from typing import Optional

def download_file(url: str, destination: Path) -> bool:
    """Download a file from URL to destination."""
    try:
        print(f"📥 Downloading {url}...")
        urllib.request.urlretrieve(url, destination)
        print(f"✅ Downloaded to {destination}")
        return True
    except Exception as e:
        print(f"❌ Failed to download {url}: {e}")
        return False

def extract_zip(zip_path: Path, extract_to: Path) -> bool:
    """Extract a zip file to the specified directory."""
    try:
        print(f"📦 Extracting {zip_path}...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
        print(f"✅ Extracted to {extract_to}")
        return True
    except Exception as e:
        print(f"❌ Failed to extract {zip_path}: {e}")
        return False

def setup_android_platform_tools():
    """Download and setup Android Platform Tools (ADB)."""
    print("🔧 Setting up Android Platform Tools...")
    
    tools_dir = Path("assets/tools")
    tools_dir.mkdir(exist_ok=True)
    
    android_tools_dir = tools_dir / "android-platform-tools"
    android_tools_dir.mkdir(exist_ok=True)
    
    # Download Android Platform Tools
    # Note: This URL may need to be updated with the latest version
    platform_tools_url = "https://dl.google.com/android/repository/platform-tools-latest-windows.zip"
    platform_tools_zip = android_tools_dir / "platform-tools.zip"
    
    if not platform_tools_zip.exists():
        if not download_file(platform_tools_url, platform_tools_zip):
            return False
    
    # Extract platform tools
    if not extract_zip(platform_tools_zip, android_tools_dir):
        return False
    
    # Remove the zip file after extraction
    platform_tools_zip.unlink()
    
    # Find the extracted directory
    extracted_dirs = [d for d in android_tools_dir.iterdir() if d.is_dir() and d.name.startswith("platform-tools")]
    if extracted_dirs:
        extracted_dir = extracted_dirs[0]
        # Move contents to android_tools_dir
        for item in extracted_dir.iterdir():
            shutil.move(str(item), str(android_tools_dir / item.name))
        extracted_dir.rmdir()
    
    print("✅ Android Platform Tools setup complete")
    return True

def create_android_path_script():
    """Create a script to add Android tools to PATH."""
    print("🔧 Creating Android PATH setup script...")
    
    tools_dir = Path("assets/tools").absolute()
    
    # Create PowerShell script
    ps_script_content = f"""# PowerShell script to add Android tools to PATH
$toolsDir = "{tools_dir}"

# Add Android Platform Tools to PATH
$androidToolsDir = Join-Path $toolsDir "android-platform-tools"
if (Test-Path $androidToolsDir) {{
    $env:PATH = "$androidToolsDir;$env:PATH"
    Write-Host "Added Android Platform Tools to PATH: $androidToolsDir"
}}

Write-Host "Android development tools are now available in this session"
Write-Host "To make permanent, add these paths to your system PATH environment variable"
"""
    
    ps_script_path = Path("scripts/utilities/setup_android_path.ps1")
    ps_script_path.parent.mkdir(exist_ok=True)
    ps_script_path.write_text(ps_script_content)
    
    # Create batch script
    bat_script_content = f"""@echo off
REM Batch script to add Android tools to PATH
set TOOLS_DIR={tools_dir}

REM Add Android Platform Tools to PATH
set ANDROID_TOOLS_DIR=%TOOLS_DIR%\\android-platform-tools
if exist "%ANDROID_TOOLS_DIR%" (
    set PATH=%ANDROID_TOOLS_DIR%;%PATH%
    echo Added Android Platform Tools to PATH: %ANDROID_TOOLS_DIR%
)

echo Android development tools are now available in this session
echo To make permanent, add these paths to your system PATH environment variable
"""
    
    bat_script_path = Path("scripts/utilities/setup_android_path.bat")
    bat_script_path.write_text(bat_script_content)
    
    print("✅ Android PATH setup scripts created")
    return True

def create_dynamic_analysis_guide():
    """Create a comprehensive guide for dynamic analysis."""
    print("📝 Creating dynamic analysis guide...")
    
    guide_content = """# MarsPro Dynamic Analysis Guide

## Prerequisites

### Required Hardware
1. **Rooted Android Device**
   - Android 7.0 or higher recommended
   - Root access required for Frida server
   - USB debugging enabled

2. **Physical MarsPro Device**
   - Any MarsPro hydroponics controller
   - Powered on and in range
   - Bluetooth enabled

3. **Computer**
   - Windows/Linux/macOS
   - USB cable for device connection
   - Internet connection for tool downloads

### Required Software
1. **Android SDK Platform Tools (ADB)**
   - Installed via setup script
   - Added to system PATH

2. **Frida**
   - Python package: `pip install frida-tools`
   - Frida server for Android (requires root)

3. **Network Monitoring Tools**
   - Wireshark or similar
   - Burp Suite (optional)

## Setup Instructions

### Step 1: Install Android Tools
```bash
python scripts/utilities/setup_android_tools.py
```

### Step 2: Setup PATH
```bash
# PowerShell
.\\scripts\\utilities\\setup_android_path.ps1

# Batch
.\\scripts\\utilities\\setup_android_path.bat
```

### Step 3: Install Frida Server on Android Device
1. Download Frida server for your Android architecture
2. Push to device: `adb push frida-server /data/local/tmp/`
3. Make executable: `adb shell chmod 755 /data/local/tmp/frida-server`
4. Start server: `adb shell su -c '/data/local/tmp/frida-server &'`

### Step 4: Verify Setup
```bash
# Check ADB
adb devices

# Check Frida
frida --version

# Check device connection
adb shell ps | grep frida
```

## Dynamic Analysis Workflow

### Phase 1: Device Discovery
1. **Scan for BLE devices**
   ```bash
   frida -U -f com.marspro.meizhi -l scripts/frida/enhanced_ble_hook.js
   ```

2. **Monitor device discovery**
   - Look for BLE scanning operations
   - Note device addresses and names
   - Document advertising data

### Phase 2: Connection Analysis
1. **Connect to MarsPro device**
   - Use the MarsPro app to connect
   - Monitor connection establishment
   - Document service discovery

2. **Service enumeration**
   - Capture all service UUIDs
   - Document characteristic UUIDs
   - Note property flags (read/write/notify)

### Phase 3: Protocol Analysis
1. **Command sending**
   - Use app to control devices
   - Monitor characteristic writes
   - Document command formats

2. **Data reading**
   - Monitor characteristic reads
   - Capture sensor data formats
   - Document notification patterns

### Phase 4: Network Analysis
1. **API endpoint discovery**
   - Monitor HTTP requests
   - Document Firebase endpoints
   - Capture authentication flows

2. **Data synchronization**
   - Monitor cloud sync operations
   - Document data formats
   - Understand update mechanisms

## Expected Findings

### BLE Communication
- **Service UUIDs**: Main control service
- **Characteristic UUIDs**: Commands, data, configuration
- **Data Formats**: Binary command structures
- **Security**: Authentication mechanisms

### Network Communication
- **Firebase Endpoints**: Authentication, data sync
- **API Formats**: JSON request/response structures
- **Authentication**: Token-based or certificate-based
- **Data Flow**: Real-time vs batch synchronization

## Documentation

### Required Outputs
1. **BLE Protocol Specification**
   - Service and characteristic UUIDs
   - Command formats and structures
   - Data formats and parsing
   - Error handling

2. **API Documentation**
   - Endpoint URLs and methods
   - Request/response formats
   - Authentication mechanisms
   - Rate limiting

3. **Implementation Guide**
   - Python BLE client example
   - Home Assistant integration
   - Error handling patterns
   - Testing procedures

## Troubleshooting

### Common Issues
1. **Device not detected**
   - Check Bluetooth permissions
   - Verify device is advertising
   - Check Frida server is running

2. **Connection failures**
   - Verify device is in range
   - Check authentication requirements
   - Monitor error messages

3. **No data captured**
   - Verify hooks are installed
   - Check characteristic properties
   - Monitor notification subscriptions

### Debug Commands
```bash
# Check device status
adb shell dumpsys bluetooth

# Monitor BLE logs
adb logcat | grep -i bluetooth

# Check Frida server
adb shell ps | grep frida

# Monitor network
adb shell tcpdump -i any -w /sdcard/capture.pcap
```

## Next Steps

### After Dynamic Analysis
1. **Implement BLE Client**
   - Create Python library
   - Support device discovery
   - Implement command sending

2. **Develop Home Assistant Integration**
   - Create custom component
   - Implement device entities
   - Add configuration flow

3. **Testing and Validation**
   - Test with real devices
   - Validate all features
   - Performance testing

---

**Version**: 1.0  
**Last Updated**: [Date]  
**Status**: Ready for Implementation
"""
    
    guide_path = Path("analysis/dynamic_analysis_guide.md")
    guide_path.write_text(guide_content)
    print(f"✅ Created dynamic analysis guide: {guide_path}")
    return True

def main():
    """Main setup function."""
    print("🚀 Setting up Android development tools for MarsPro analysis")
    print("=" * 60)
    
    # Setup tools
    success = True
    success &= setup_android_platform_tools()
    success &= create_android_path_script()
    success &= create_dynamic_analysis_guide()
    
    if success:
        print("\n🎉 Android tools setup complete!")
        print("\n📋 Next steps:")
        print("1. Run the PATH setup script:")
        print("   .\\scripts\\utilities\\setup_android_path.ps1")
        print("2. Install Frida server on your rooted Android device")
        print("3. Follow the dynamic analysis guide:")
        print("   analysis\\dynamic_analysis_guide.md")
        print("\n📁 Tools installed in: assets/tools/android-platform-tools/")
    else:
        print("\n❌ Some tools failed to install. Please check the errors above.")
    
    return success

if __name__ == "__main__":
    main() 