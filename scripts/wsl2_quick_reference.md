# WSL2 BLE Emulator - Quick Reference

## 🚀 Essential Commands

### **Windows PowerShell (Administrator)**
```powershell
# Enable WSL2
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart

# Restart computer, then:
wsl --set-default-version 2
wsl --install -d Ubuntu
```

### **WSL2 Ubuntu Setup**
```bash
# Navigate to project
cd /mnt/c/Users/marvi/Coding/MarsPro

# Run setup script
chmod +x scripts/setup_wsl2_ble_emulator.sh
./scripts/setup_wsl2_ble_emulator.sh
```

### **Start BLE Emulator**
```bash
# Navigate to emulator
cd ~/marspro_ble_emulator

# Activate environment
source ~/marspro_ble_env/bin/activate

# Start emulator
python3 marspro_gatt_server.py
```

### **Test BLE Scanner**
```bash
# In another terminal
cd ~/marspro_ble_emulator
source ~/marspro_ble_env/bin/activate
python3 test_ble_scan.py
```

## 🔧 Troubleshooting Commands

### **Bluetooth Issues**
```bash
# Check Bluetooth adapter
hciconfig

# Restart Bluetooth service
sudo systemctl restart bluetooth

# Add user to bluetooth group
sudo usermod -a -G bluetooth $USER
```

### **WSL2 Management**
```bash
# Shutdown WSL2
wsl --shutdown

# List WSL distributions
wsl --list --verbose

# Restart WSL2
wsl
```

### **Python Environment**
```bash
# Reinstall dependencies
pip install --upgrade pip
pip install bleak dbus-next pydbus PyGObject

# Check Python version
python3 --version
```

## 📊 Monitoring Commands

### **View Logs**
```bash
# Real-time logs (in emulator terminal)
# Shows BLE traffic automatically

# View saved logs
cat ~/marspro_ble_emulator/ble_traffic_log.json

# Monitor system logs
sudo journalctl -u bluetooth -f
```

### **Check Services**
```bash
# Check Bluetooth service
sudo systemctl status bluetooth

# Check DBus service
sudo systemctl status dbus

# List all services
sudo systemctl list-units --type=service
```

## 🎯 Success Checklist

- [ ] WSL2 Ubuntu installed and running
- [ ] Setup script completed without errors
- [ ] BLE emulator starts: "MarsPro BLE GATT Server is running!"
- [ ] Device advertises: "Device is now advertising as 'MarsPro Controller'"
- [ ] BLE scanner finds the device
- [ ] MarsPro app can connect to emulator

## 📱 Testing Steps

1. **Enable Bluetooth** on your phone
2. **Open MarsPro app**
3. **Scan for devices**
4. **Look for "MarsPro Controller"**
5. **Connect and test functions**

## 🚨 Common Issues

### **"No Bluetooth adapter found"**
- Check Windows Bluetooth settings
- Ensure computer has Bluetooth capability
- Windows 11 has better support

### **"Permission denied"**
```bash
sudo usermod -a -G bluetooth $USER
# Log out and back in
```

### **"Module not found"**
```bash
source ~/marspro_ble_env/bin/activate
pip install --upgrade pip
pip install bleak dbus-next pydbus PyGObject
```

### **"Service not found"**
```bash
sudo systemctl start bluetooth
sudo systemctl enable bluetooth
```

## 📁 Key Files

- `~/marspro_ble_emulator/marspro_gatt_server.py` - Main emulator
- `~/marspro_ble_emulator/test_ble_scan.py` - BLE scanner
- `~/marspro_ble_emulator/ble_traffic_log.json` - Traffic logs
- `~/marspro_ble_emulator/README.md` - Usage instructions

## ⏱️ Time Estimates

- **WSL2 Setup**: 10-15 minutes
- **Ubuntu Installation**: 5-10 minutes
- **BLE Setup Script**: 10-15 minutes
- **Testing**: 5-10 minutes
- **Total**: 30-50 minutes

---

**Remember**: Run PowerShell as Administrator for WSL2 setup! 