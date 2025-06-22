@echo off
REM MarsPro BLE Emulator Setup - All Commands
REM This batch file contains all the commands needed for BLE emulation setup

echo ========================================
echo MarsPro BLE Emulator Setup
echo ========================================
echo.

echo [1/4] Checking Python and dependencies...
python --version
pip install bleak

echo.
echo [2/4] Testing BLE scanner...
python scripts/marspro_ble_analyzer.py

echo.
echo [3/4] Creating analysis directory...
mkdir analysis 2>nul

echo.
echo [4/4] Setup complete!
echo.
echo ========================================
echo NEXT STEPS:
echo ========================================
echo.
echo OPTION 1 (IMMEDIATE - 15 min):
echo 1. Install "nRF Connect for Mobile" on Android
echo 2. Create GATT Server with MarsPro UUIDs
echo 3. Start advertising as "MarsPro Controller"
echo 4. Test with MarsPro app
echo.
echo OPTION 2 (FULL DEVELOPMENT - 1-2 hours):
echo 1. Run PowerShell as Administrator
echo 2. Execute WSL2 setup commands
echo 3. Install Ubuntu in WSL2
echo 4. Run setup script: scripts/setup_wsl2_ble_emulator.sh
echo.
echo See analysis/complete_ble_solution.md for full details
echo.
pause 