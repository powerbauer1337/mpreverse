#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Comprehensive WSL2 Fix Script for MarsPro Project
    
.DESCRIPTION
    This script fixes common WSL2 issues and sets up a proper environment for BLE emulation.
    It handles installation, configuration, and troubleshooting of WSL2.
    
.PARAMETER Force
    Force reinstallation of WSL2 components
    
.PARAMETER InstallUbuntu
    Automatically install Ubuntu after WSL2 setup
    
.EXAMPLE
    .\fix_wsl2.ps1 -Force -InstallUbuntu
#>

param(
    [switch]$Force,
    [switch]$InstallUbuntu
)

# Ensure script runs with administrator privileges
if (-NOT ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Host "This script requires administrator privileges. Please run as Administrator." -ForegroundColor Red
    Write-Host "Right-click PowerShell and select 'Run as Administrator'" -ForegroundColor Yellow
    exit 1
}

Write-Host "=== MarsPro WSL2 Fix Script ===" -ForegroundColor Green
Write-Host "Starting comprehensive WSL2 fix..." -ForegroundColor Cyan

# Function to check if a command exists
function Test-Command($cmdname) {
    return [bool](Get-Command -Name $cmdname -ErrorAction SilentlyContinue)
}

# Function to write colored output
function Write-Status($message, $status) {
    $color = if ($status -eq "OK") { "Green" } elseif ($status -eq "WARNING") { "Yellow" } else { "Red" }
    Write-Host "[$status] $message" -ForegroundColor $color
}

# Step 1: Check Windows version
Write-Host "`n1. Checking Windows version..." -ForegroundColor Cyan
$osInfo = Get-ComputerInfo
$buildNumber = $osInfo.WindowsBuildLabEx.Split('.')[0]
Write-Status "Windows Build: $buildNumber" "OK"

if ($buildNumber -lt 19041) {
    Write-Status "WSL2 requires Windows 10 version 2004 or higher (Build 19041+)" "ERROR"
    Write-Host "Please update Windows to use WSL2" -ForegroundColor Red
    exit 1
}

# Step 2: Enable Windows Subsystem for Linux
Write-Host "`n2. Enabling Windows Subsystem for Linux..." -ForegroundColor Cyan
try {
    $wslFeature = Get-WindowsOptionalFeature -Online -FeatureName Microsoft-Windows-Subsystem-Linux
    if ($wslFeature.State -eq "Enabled") {
        Write-Status "WSL feature already enabled" "OK"
    } else {
        Write-Host "Enabling WSL feature..." -ForegroundColor Yellow
        Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Windows-Subsystem-Linux -All -NoRestart
        Write-Status "WSL feature enabled successfully" "OK"
    }
} catch {
    Write-Status "Failed to check/enable WSL feature: $($_.Exception.Message)" "ERROR"
    Write-Host "Trying alternative method..." -ForegroundColor Yellow
    
    # Alternative method using DISM
    try {
        $result = dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
        if ($LASTEXITCODE -eq 0) {
            Write-Status "WSL feature enabled using DISM" "OK"
        } else {
            Write-Status "Failed to enable WSL feature using DISM" "ERROR"
        }
    } catch {
        Write-Status "Failed to enable WSL feature: $($_.Exception.Message)" "ERROR"
    }
}

# Step 3: Enable Virtual Machine Platform
Write-Host "`n3. Enabling Virtual Machine Platform..." -ForegroundColor Cyan
try {
    $vmFeature = Get-WindowsOptionalFeature -Online -FeatureName VirtualMachinePlatform
    if ($vmFeature.State -eq "Enabled") {
        Write-Status "Virtual Machine Platform already enabled" "OK"
    } else {
        Write-Host "Enabling Virtual Machine Platform..." -ForegroundColor Yellow
        Enable-WindowsOptionalFeature -Online -FeatureName VirtualMachinePlatform -All -NoRestart
        Write-Status "Virtual Machine Platform enabled successfully" "OK"
    }
} catch {
    Write-Status "Failed to check/enable Virtual Machine Platform: $($_.Exception.Message)" "ERROR"
    Write-Host "Trying alternative method..." -ForegroundColor Yellow
    
    # Alternative method using DISM
    try {
        $result = dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
        if ($LASTEXITCODE -eq 0) {
            Write-Status "Virtual Machine Platform enabled using DISM" "OK"
        } else {
            Write-Status "Failed to enable Virtual Machine Platform using DISM" "ERROR"
        }
    } catch {
        Write-Status "Failed to enable Virtual Machine Platform: $($_.Exception.Message)" "ERROR"
    }
}

# Step 4: Check if WSL command is available
Write-Host "`n4. Checking WSL command availability..." -ForegroundColor Cyan
if (Test-Command "wsl") {
    Write-Status "WSL command available" "OK"
} else {
    Write-Status "WSL command not available - may need restart" "WARNING"
    Write-Host "Please restart your computer and run this script again" -ForegroundColor Yellow
    exit 1
}

# Step 5: Set WSL2 as default
Write-Host "`n5. Setting WSL2 as default..." -ForegroundColor Cyan
try {
    $result = wsl --set-default-version 2
    if ($LASTEXITCODE -eq 0) {
        Write-Status "WSL2 set as default version" "OK"
    } else {
        Write-Status "Failed to set WSL2 as default" "ERROR"
        Write-Host "This might be normal if no distributions are installed yet" -ForegroundColor Yellow
    }
} catch {
    Write-Status "Failed to set WSL2 as default: $($_.Exception.Message)" "ERROR"
}

# Step 6: Check current WSL status
Write-Host "`n6. Checking current WSL status..." -ForegroundColor Cyan
try {
    $wslStatus = wsl --status
    Write-Host "WSL Status:" -ForegroundColor Green
    Write-Host $wslStatus -ForegroundColor White
} catch {
    Write-Status "Failed to get WSL status: $($_.Exception.Message)" "WARNING"
}

# Step 7: List installed distributions
Write-Host "`n7. Checking installed distributions..." -ForegroundColor Cyan
try {
    $distributions = wsl --list --verbose
    if ($distributions) {
        Write-Host "Installed distributions:" -ForegroundColor Green
        Write-Host $distributions -ForegroundColor White
    } else {
        Write-Status "No distributions installed" "WARNING"
    }
} catch {
    Write-Status "Failed to list distributions: $($_.Exception.Message)" "WARNING"
}

# Step 8: Install Ubuntu if requested
if ($InstallUbuntu) {
    Write-Host "`n8. Installing Ubuntu..." -ForegroundColor Cyan
    try {
        Write-Host "Downloading and installing Ubuntu..." -ForegroundColor Yellow
        $result = wsl --install -d Ubuntu
        if ($LASTEXITCODE -eq 0) {
            Write-Status "Ubuntu installation initiated successfully" "OK"
            Write-Host "Please complete the Ubuntu setup when prompted" -ForegroundColor Green
        } else {
            Write-Status "Failed to install Ubuntu" "ERROR"
        }
    } catch {
        Write-Status "Failed to install Ubuntu: $($_.Exception.Message)" "ERROR"
    }
}

# Step 9: Check Hyper-V and virtualization
Write-Host "`n9. Checking virtualization support..." -ForegroundColor Cyan
try {
    $hyperV = Get-WindowsOptionalFeature -Online -FeatureName Microsoft-Hyper-V-All
    if ($hyperV.State -eq "Enabled") {
        Write-Status "Hyper-V is enabled" "OK"
    } else {
        Write-Status "Hyper-V is not enabled (not required for WSL2)" "OK"
    }
    
    # Check if virtualization is enabled in BIOS
    $vmSupport = Get-ComputerInfo | Select-Object -ExpandProperty HyperVRequirementVirtualizationFirmwareEnabled
    if ($vmSupport) {
        Write-Status "Virtualization enabled in BIOS" "OK"
    } else {
        Write-Status "Virtualization may not be enabled in BIOS" "WARNING"
        Write-Host "Please enable virtualization (VT-x/AMD-V) in your BIOS settings" -ForegroundColor Yellow
    }
} catch {
    Write-Status "Failed to check virtualization support: $($_.Exception.Message)" "WARNING"
}

# Step 10: Update WSL kernel if needed
Write-Host "`n10. Checking WSL kernel..." -ForegroundColor Cyan
try {
    $kernelUpdate = wsl --update
    if ($LASTEXITCODE -eq 0) {
        Write-Status "WSL kernel updated successfully" "OK"
    } else {
        Write-Status "WSL kernel update failed or not needed" "WARNING"
    }
} catch {
    Write-Status "Failed to update WSL kernel: $($_.Exception.Message)" "WARNING"
}

# Step 11: Create MarsPro WSL setup script
Write-Host "`n11. Creating MarsPro WSL setup script..." -ForegroundColor Cyan
$setupScript = @"
#!/bin/bash
# MarsPro WSL2 Setup Script
# This script sets up the BLE emulation environment in WSL2

echo "=== MarsPro WSL2 BLE Emulator Setup ==="

# Update package list
echo "Updating package list..."
sudo apt update

# Install required packages
echo "Installing required packages..."
sudo apt install -y bluez bluez-tools bluetooth libbluetooth-dev \
    python3 python3-pip python3-venv git curl wget \
    build-essential cmake pkg-config libssl-dev \
    libusb-1.0-0-dev libudev-dev

# Install Python packages
echo "Installing Python packages..."
pip3 install bleak asyncio-mqtt paho-mqtt

# Enable Bluetooth service
echo "Enabling Bluetooth service..."
sudo systemctl enable bluetooth
sudo systemctl start bluetooth

# Create MarsPro directory
echo "Creating MarsPro directory..."
mkdir -p ~/marspro
cd ~/marspro

# Clone or copy MarsPro files
echo "Setting up MarsPro files..."
# Note: You'll need to copy files from Windows to WSL2

echo "WSL2 setup complete!"
echo "Next steps:"
echo "1. Copy MarsPro files from Windows to WSL2"
echo "2. Run the BLE emulator script"
echo "3. Test BLE functionality"
"@

$setupScriptPath = "scripts/wsl2_setup.sh"
$setupScript | Out-File -FilePath $setupScriptPath -Encoding UTF8
Write-Status "Created WSL2 setup script: $setupScriptPath" "OK"

# Step 12: Final status check
Write-Host "`n12. Final status check..." -ForegroundColor Cyan
try {
    $finalStatus = wsl --status
    Write-Host "Final WSL Status:" -ForegroundColor Green
    Write-Host $finalStatus -ForegroundColor White
    
    Write-Status "WSL2 fix completed successfully!" "OK"
    Write-Host "`nNext steps:" -ForegroundColor Cyan
    Write-Host "1. Restart your computer if prompted" -ForegroundColor Yellow
    Write-Host "2. Install Ubuntu: wsl --install -d Ubuntu" -ForegroundColor Yellow
    Write-Host "3. Run the WSL2 setup script: bash scripts/wsl2_setup.sh" -ForegroundColor Yellow
    Write-Host "4. Test BLE functionality in WSL2" -ForegroundColor Yellow
    
} catch {
    Write-Status "Failed to get final status: $($_.Exception.Message)" "WARNING"
}

Write-Host "`n=== WSL2 Fix Complete ===" -ForegroundColor Green 