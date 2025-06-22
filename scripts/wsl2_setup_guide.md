# WSL2 BLE Emulator Setup Guide

## 🚀 Complete Setup Process

### **Phase 1: Enable WSL2 (Administrator Required)**

1. **Open PowerShell as Administrator**
   - Press `Windows + X`
   - Select "Windows PowerShell (Admin)" or "Terminal (Admin)"

2. **Enable WSL Features**
   ```powershell
   dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
   dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
   ```

3. **Restart Your Computer**
   - Save any work and restart
   - This is required for the features to take effect

### **Phase 2: Install Ubuntu**

1. **After Restart, Open PowerShell as Administrator**

2. **Set WSL2 as Default**
   ```powershell
   wsl --set-default-version 2
   ```

3. **Install Ubuntu**
   ```powershell
   wsl --install -d Ubuntu
   ```

4. **Wait for Installation**
   - Ubuntu will download and install
   - This may take several minutes

5. **Complete Ubuntu Setup**
   - When prompted, create a username and password
   - Remember these credentials

### **Phase 3: Run the BLE Emulator Setup**

1. **Open WSL2 Ubuntu**
   - You can open it from Start Menu or run `wsl` in PowerShell

2. **Navigate to Your Project**
   ```bash
   cd /mnt/c/Users/marvi/Coding/MarsPro
   ```

3. **Make Setup Script Executable**
   ```bash
   chmod +x scripts/setup_wsl2_ble_emulator.sh
   ```

4. **Run the Setup Script**
   ```bash
   ./scripts/setup_wsl2_ble_emulator.sh
   ```

5. **Wait for Installation**
   - The script will install all required packages
   - This may take 10-15 minutes
   - You'll see progress messages

### **Phase 4: Start the BLE Emulator**

1. **Navigate to Emulator Directory**
   ```bash
   cd ~/marspro_ble_emulator
   ```

2. **Activate Python Environment**
   ```bash
   source ~/marspro_ble_env/bin/activate
   ```

3. **Start the BLE Emulator**
   ```bash
   python3 marspro_gatt_server.py
   ```

4. **Verify It's Running**
   - You should see: "MarsPro BLE GATT Server is running!"
   - "Device is now advertising as 'MarsPro Controller'"

### **Phase 5: Test the Emulator**

1. **Open Another WSL2 Terminal**
   - Open a new terminal or WSL2 window

2. **Test BLE Scanner**
   ```bash
   cd ~/marspro_ble_emulator
   source ~/marspro_ble_env/bin/activate
   python3 test_ble_scan.py
   ```

3. **Test with MarsPro App**
   - Open MarsPro app on your phone
   - Scan for BLE devices
   - Look for "MarsPro Controller"

## 🔧 Troubleshooting

### **WSL2 Installation Issues**

**Error: "WSL2 will be installed on your system"**
- This is normal, just wait for the installation to complete

**Error: "Virtualization not enabled"**
- Enable virtualization in BIOS (Intel VT-x or AMD-V)
- Restart and try again

**Error: "Hyper-V not installed"**
- The commands above should fix this
- Make sure to restart after running them

### **Bluetooth Issues**

**No Bluetooth adapter found**
- Ensure Bluetooth is enabled in Windows
- Check if your computer has Bluetooth capability
- Windows 11 has better WSL2 Bluetooth support

**Permission denied errors**
```bash
sudo usermod -a -G bluetooth $USER
```
Then log out and back in to WSL2

**Bluetooth service won't start**
```bash
sudo systemctl restart bluetooth
```

### **Python/Dependencies Issues**

**Module not found errors**
```bash
cd ~/marspro_ble_emulator
source ~/marspro_ble_env/bin/activate
pip install --upgrade pip
pip install -r requirements.txt  # if available
```

**DBus errors**
```bash
sudo systemctl start dbus
sudo systemctl enable dbus
```

## 📱 Testing with MarsPro App

1. **Ensure Bluetooth is enabled** on your phone
2. **Open MarsPro app**
3. **Go to device discovery/scan**
4. **Look for "MarsPro Controller"**
5. **Try to connect to it**
6. **Test basic functions** (on/off, status, etc.)

## 📊 Monitoring and Logs

### **View Real-time Logs**
The emulator shows real-time BLE traffic in the terminal:
```
BLE Traffic: IN write on 0000ffe1-0000-1000-8000-00805f9b34fb = 01
BLE Traffic: OUT notify on 0000ffe2-0000-1000-8000-00805f9b34fb = 0102030405
```

### **Save Traffic Logs**
When you stop the emulator (Ctrl+C), it saves logs to:
```
~/marspro_ble_emulator/ble_traffic_log.json
```

### **View Logs**
```bash
cat ~/marspro_ble_emulator/ble_traffic_log.json
```

## 🎯 Success Indicators

- ✅ WSL2 Ubuntu is running
- ✅ Setup script completed without errors
- ✅ BLE emulator starts without errors
- ✅ "MarsPro Controller" appears in BLE scans
- ✅ MarsPro app can connect to emulator
- ✅ Basic commands work (device info, status)

## 🚀 Next Steps After Setup

1. **Document Protocol Patterns**
   - Monitor BLE traffic when using MarsPro app
   - Document command structures and responses

2. **Implement More Commands**
   - Add more sophisticated command handling
   - Implement device state management

3. **Test Home Assistant Integration**
   - Use emulator to test Home Assistant component
   - Validate protocol implementation

4. **Automated Testing**
   - Create automated test scenarios
   - Validate all device functions

## 📞 Getting Help

If you encounter issues:

1. **Check the troubleshooting section above**
2. **Look at the error messages carefully**
3. **Ensure all prerequisites are met**
4. **Try restarting WSL2**: `wsl --shutdown` then restart
5. **Check Windows Bluetooth settings**

---

**Expected Time**: 30-60 minutes for complete setup
**Difficulty**: Medium (requires administrator access)
**Outcome**: Full programmable MarsPro BLE emulator 