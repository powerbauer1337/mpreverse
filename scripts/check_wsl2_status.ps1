#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Check WSL2 Status Script for MarsPro Project
    
.DESCRIPTION
    This script checks the current status of WSL2 without requiring administrator privileges.
    It provides diagnostic information about WSL2 installation and configuration.
#>

Write-Host "=== MarsPro WSL2 Status Check ===" -ForegroundColor Green
Write-Host "Checking WSL2 status..." -ForegroundColor Cyan

# Function to write colored output
function Write-Status($message, $status) {
    $color = if ($status -eq "OK") { "Green" } elseif ($status -eq "WARNING") { "Yellow" } else { "Red" }
    Write-Host "[$status] $message" -ForegroundColor $color
}

# Function to check if a command exists
function Test-Command($cmdname) {
    return [bool](Get-Command -Name $cmdname -ErrorAction SilentlyContinue)
}

# Check Windows version
Write-Host "`n1. Windows Version Check:" -ForegroundColor Cyan
try {
    $osInfo = Get-ComputerInfo
    $buildNumber = $osInfo.WindowsBuildLabEx.Split('.')[0]
    Write-Status "Windows Build: $buildNumber" "OK"
    
    if ($buildNumber -lt 19041) {
        Write-Status "WSL2 requires Windows 10 version 2004 or higher (Build 19041+)" "ERROR"
    } else {
        Write-Status "Windows version supports WSL2" "OK"
    }
} catch {
    Write-Status "Failed to get Windows version: $($_.Exception.Message)" "ERROR"
}

# Check if WSL command is available
Write-Host "`n2. WSL Command Availability:" -ForegroundColor Cyan
if (Test-Command "wsl") {
    Write-Status "WSL command is available" "OK"
} else {
    Write-Status "WSL command is not available" "ERROR"
    Write-Host "WSL may not be installed or enabled" -ForegroundColor Yellow
}

# Check WSL status
Write-Host "`n3. WSL Status:" -ForegroundColor Cyan
try {
    $wslStatus = wsl --status
    if ($wslStatus) {
        Write-Host "WSL Status Output:" -ForegroundColor Green
        Write-Host $wslStatus -ForegroundColor White
    } else {
        Write-Status "No WSL status output" "WARNING"
    }
} catch {
    Write-Status "Failed to get WSL status: $($_.Exception.Message)" "ERROR"
}

# Check installed distributions
Write-Host "`n4. Installed Distributions:" -ForegroundColor Cyan
try {
    $distributions = wsl --list --verbose
    if ($distributions) {
        Write-Host "Installed distributions:" -ForegroundColor Green
        Write-Host $distributions -ForegroundColor White
    } else {
        Write-Status "No distributions installed" "WARNING"
    }
} catch {
    Write-Status "Failed to list distributions: $($_.Exception.Message)" "ERROR"
}

# Check virtualization support
Write-Host "`n5. Virtualization Support:" -ForegroundColor Cyan
try {
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

# Check Windows features (read-only)
Write-Host "`n6. Windows Features:" -ForegroundColor Cyan
try {
    $wslFeature = Get-WindowsOptionalFeature -Online -FeatureName Microsoft-Windows-Subsystem-Linux
    if ($wslFeature.State -eq "Enabled") {
        Write-Status "WSL feature is enabled" "OK"
    } else {
        Write-Status "WSL feature is not enabled" "ERROR"
    }
} catch {
    Write-Status "Failed to check WSL feature: $($_.Exception.Message)" "WARNING"
}

try {
    $vmFeature = Get-WindowsOptionalFeature -Online -FeatureName VirtualMachinePlatform
    if ($vmFeature.State -eq "Enabled") {
        Write-Status "Virtual Machine Platform is enabled" "OK"
    } else {
        Write-Status "Virtual Machine Platform is not enabled" "ERROR"
    }
} catch {
    Write-Status "Failed to check Virtual Machine Platform: $($_.Exception.Message)" "WARNING"
}

# Check if running as administrator
Write-Host "`n7. Administrator Privileges:" -ForegroundColor Cyan
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")
if ($isAdmin) {
    Write-Status "Running with administrator privileges" "OK"
} else {
    Write-Status "Not running with administrator privileges" "WARNING"
    Write-Host "Some WSL2 operations require administrator privileges" -ForegroundColor Yellow
}

# Summary and recommendations
Write-Host "`n=== Summary and Recommendations ===" -ForegroundColor Green

if (Test-Command "wsl") {
    Write-Host "✅ WSL is available" -ForegroundColor Green
} else {
    Write-Host "❌ WSL is not available" -ForegroundColor Red
    Write-Host "   Run: .\scripts\fix_wsl2.ps1 (as Administrator)" -ForegroundColor Yellow
}

try {
    $distributions = wsl --list --verbose
    if ($distributions) {
        Write-Host "✅ WSL distributions are installed" -ForegroundColor Green
    } else {
        Write-Host "⚠️  No WSL distributions installed" -ForegroundColor Yellow
        Write-Host "   Run: wsl --install -d Ubuntu" -ForegroundColor Yellow
    }
} catch {
    Write-Host "❌ Cannot check WSL distributions" -ForegroundColor Red
}

Write-Host "`nNext Steps:" -ForegroundColor Cyan
Write-Host "1. If WSL is not working, run: .\scripts\fix_wsl2.ps1 (as Administrator)" -ForegroundColor Yellow
Write-Host "2. If no distributions are installed, run: wsl --install -d Ubuntu" -ForegroundColor Yellow
Write-Host "3. After installation, run: bash scripts/wsl2_setup.sh" -ForegroundColor Yellow

Write-Host "`n=== Status Check Complete ===" -ForegroundColor Green 