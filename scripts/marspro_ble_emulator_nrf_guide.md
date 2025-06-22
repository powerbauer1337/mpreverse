# MarsPro BLE Emulator Setup Guide (nRF Connect)

## Overview
This guide shows how to emulate a MarsPro BLE device using nRF Connect for Mobile on an Android phone.

## Prerequisites
- Android phone with Bluetooth 4.0+
- nRF Connect for Mobile app (free from Google Play Store)

## Step 1: Install nRF Connect
1. Open Google Play Store
2. Search for "nRF Connect for Mobile"
3. Install the app by Nordic Semiconductor

## Step 2: Create GATT Server Configuration
1. Open nRF Connect for Mobile
2. Tap the menu (hamburger icon) in the top-left
3. Select "GATT Server"
4. Tap the "+" icon to create a new configuration
5. Name it "MarsPro Emulator"

## Step 3: Add MarsPro Service
1. In the GATT Server configuration, tap "Add Service"
2. Select "Custom Service"
3. Set Service UUID to: `0000ffe0-0000-1000-8000-00805f9b34fb`
4. Tap "OK"

## Step 4: Add Characteristics
Add the following characteristics to the service:

### Command Characteristic
- UUID: `0000ffe1-0000-1000-8000-00805f9b34fb`
- Properties: Write, Write Without Response
- Initial Value: `00` (empty)

### Data Characteristic
- UUID: `0000ffe2-0000-1000-8000-00805f9b34fb`
- Properties: Read, Notify
- Initial Value: `0102030405` (sample data)

### Config Characteristic
- UUID: `0000ffe3-0000-1000-8000-00805f9b34fb`
- Properties: Read, Write
- Initial Value: `0000` (empty)

### Status Characteristic
- UUID: `0000ffe4-0000-1000-8000-00805f9b34fb`
- Properties: Read, Notify
- Initial Value: `0100` (device ready)

## Step 5: Configure Advertising
1. Go to the "Advertiser" tab
2. Tap the "+" icon to create a new advertising packet
3. Set the following:
   - Name: "MarsPro Controller"
   - Enable "Scannable" and "Connectable"
   - Add "Complete Local Name" record with value "MarsPro Controller"
   - Add "Service UUID" record with value `0000ffe0-0000-1000-8000-00805f9b34fb`

## Step 6: Start Advertising
1. Enable the advertising template you just created
2. The phone will now advertise as a MarsPro device
3. Other devices can scan and connect to it

## Step 7: Test with MarsPro App
1. Open the MarsPro app on another device
2. Scan for BLE devices
3. You should see "MarsPro Controller" in the list
4. Try to connect to it

## Step 8: Monitor Traffic
1. In nRF Connect, go to the "GATT Server" tab
2. When connected, you can see:
   - Read/Write operations on characteristics
   - Data being exchanged
   - Connection status

## Troubleshooting
- Make sure Bluetooth is enabled on both devices
- Ensure the phone is not connected to another BLE device
- Check that the UUIDs match exactly
- Try restarting the advertising if connection fails

## Next Steps
Once the basic emulation is working:
1. Observe the commands sent by the MarsPro app
2. Update the characteristic values to respond appropriately
3. Document the protocol based on observed traffic
4. Implement more sophisticated responses in the emulator 