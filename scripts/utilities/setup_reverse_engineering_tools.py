#!/usr/bin/env python3
"""
Setup script for reverse engineering tools
Downloads and configures apktool, jadx, and other necessary tools
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

def setup_apktool():
    """Download and setup apktool."""
    print("🔧 Setting up apktool...")
    
    tools_dir = Path("assets/tools")
    tools_dir.mkdir(exist_ok=True)
    
    apktool_dir = tools_dir / "apktool"
    apktool_dir.mkdir(exist_ok=True)
    
    # Download apktool.jar
    apktool_jar_url = "https://bitbucket.org/iBotPeaches/apktool/downloads/apktool_2.9.3.jar"
    apktool_jar_path = apktool_dir / "apktool.jar"
    
    if not apktool_jar_path.exists():
        if not download_file(apktool_jar_url, apktool_jar_path):
            return False
    
    # Create apktool.bat for Windows
    apktool_bat_content = f"""@echo off
java -jar "%~dp0apktool.jar" %*
"""
    apktool_bat_path = apktool_dir / "apktool.bat"
    apktool_bat_path.write_text(apktool_bat_content)
    
    # Create apktool.sh for Unix-like systems
    apktool_sh_content = f"""#!/bin/bash
java -jar "$(dirname "$0")/apktool.jar" "$@"
"""
    apktool_sh_path = apktool_dir / "apktool.sh"
    apktool_sh_path.write_text(apktool_sh_content)
    
    print("✅ apktool setup complete")
    return True

def setup_jadx():
    """Download and setup jadx."""
    print("🔧 Setting up jadx...")
    
    tools_dir = Path("assets/tools")
    jadx_dir = tools_dir / "jadx"
    jadx_dir.mkdir(exist_ok=True)
    
    # Download jadx
    jadx_url = "https://github.com/skylot/jadx/releases/download/v1.4.7/jadx-1.4.7.zip"
    jadx_zip_path = jadx_dir / "jadx.zip"
    
    if not jadx_zip_path.exists():
        if not download_file(jadx_url, jadx_zip_path):
            return False
    
    # Extract jadx
    if not extract_zip(jadx_zip_path, jadx_dir):
        return False
    
    # Remove the zip file after extraction
    jadx_zip_path.unlink()
    
    # Find the extracted directory
    extracted_dirs = [d for d in jadx_dir.iterdir() if d.is_dir() and d.name.startswith("jadx")]
    if extracted_dirs:
        extracted_dir = extracted_dirs[0]
        # Move contents to jadx_dir
        for item in extracted_dir.iterdir():
            shutil.move(str(item), str(jadx_dir / item.name))
        extracted_dir.rmdir()
    
    print("✅ jadx setup complete")
    return True

def setup_frida():
    """Setup Frida tools."""
    print("🔧 Setting up Frida...")
    
    # Frida tools are installed via pip, so we just need to verify
    try:
        result = subprocess.run(["frida", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Frida is installed: {result.stdout.strip()}")
            return True
        else:
            print("⚠️  Frida not found. Install with: pip install frida-tools")
            return False
    except FileNotFoundError:
        print("⚠️  Frida not found. Install with: pip install frida-tools")
        return False

def create_path_script():
    """Create a script to add tools to PATH."""
    print("🔧 Creating PATH setup script...")
    
    tools_dir = Path("assets/tools").absolute()
    
    # Create PowerShell script
    ps_script_content = f"""# PowerShell script to add reverse engineering tools to PATH
$toolsDir = "{tools_dir}"

# Add apktool to PATH
$apktoolDir = Join-Path $toolsDir "apktool"
if (Test-Path $apktoolDir) {{
    $env:PATH = "$apktoolDir;$env:PATH"
    Write-Host "Added apktool to PATH: $apktoolDir"
}}

# Add jadx to PATH
$jadxDir = Join-Path $toolsDir "jadx\\bin"
if (Test-Path $jadxDir) {{
    $env:PATH = "$jadxDir;$env:PATH"
    Write-Host "Added jadx to PATH: $jadxDir"
}}

Write-Host "Reverse engineering tools are now available in this session"
Write-Host "To make permanent, add these paths to your system PATH environment variable"
"""
    
    ps_script_path = Path("scripts/utilities/setup_path.ps1")
    ps_script_path.parent.mkdir(exist_ok=True)
    ps_script_path.write_text(ps_script_content)
    
    # Create batch script
    bat_script_content = f"""@echo off
REM Batch script to add reverse engineering tools to PATH
set TOOLS_DIR={tools_dir}

REM Add apktool to PATH
set APKTOOL_DIR=%TOOLS_DIR%\\apktool
if exist "%APKTOOL_DIR%" (
    set PATH=%APKTOOL_DIR%;%PATH%
    echo Added apktool to PATH: %APKTOOL_DIR%
)

REM Add jadx to PATH
set JADX_DIR=%TOOLS_DIR%\\jadx\\bin
if exist "%JADX_DIR%" (
    set PATH=%JADX_DIR%;%PATH%
    echo Added jadx to PATH: %JADX_DIR%
)

echo Reverse engineering tools are now available in this session
echo To make permanent, add these paths to your system PATH environment variable
"""
    
    bat_script_path = Path("scripts/utilities/setup_path.bat")
    bat_script_path.write_text(bat_script_content)
    
    print("✅ PATH setup scripts created")
    return True

def main():
    """Main setup function."""
    print("🚀 Setting up reverse engineering tools for MarsPro analysis")
    print("=" * 60)
    
    # Check if Java is available
    try:
        result = subprocess.run(["java", "-version"], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Java is available")
        else:
            print("❌ Java not found. Please install Java 8 or higher")
            return False
    except FileNotFoundError:
        print("❌ Java not found. Please install Java 8 or higher")
        return False
    
    # Setup tools
    success = True
    success &= setup_apktool()
    success &= setup_jadx()
    success &= setup_frida()
    success &= create_path_script()
    
    if success:
        print("\n🎉 Reverse engineering tools setup complete!")
        print("\n📋 Next steps:")
        print("1. Run the PATH setup script:")
        print("   .\\scripts\\utilities\\setup_path.ps1")
        print("2. Start the reverse engineering analysis:")
        print("   python scripts\\analyze.py assets\\apks\\MarsPro_1.3.2_APKPure.xapk")
        print("\n📁 Tools installed in: assets/tools/")
    else:
        print("\n❌ Some tools failed to install. Please check the errors above.")
    
    return success

if __name__ == "__main__":
    main() 