// Frida script to hook BLE operations in MarsPro app
// This script captures BLE communication patterns for reverse engineering

console.log("[+] MarsPro BLE Hook Loaded");

// Hook BLE characteristic operations
Java.perform(function() {
    console.log("[+] Starting BLE hooks...");
    
    // Hook BluetoothGattCharacteristic operations
    try {
        var BluetoothGattCharacteristic = Java.use("android.bluetooth.BluetoothGattCharacteristic");
        
        // Hook readCharacteristic
        BluetoothGattCharacteristic.getValue.implementation = function() {
            var result = this.getValue();
            console.log("[BLE] Read Characteristic:");
            console.log("  UUID: " + this.getUuid());
            console.log("  Value: " + bytes2hex(result));
            console.log("  Service UUID: " + this.getService().getUuid());
            return result;
        };
        
        // Hook setValue
        BluetoothGattCharacteristic.setValue.implementation = function(value) {
            console.log("[BLE] Write Characteristic:");
            console.log("  UUID: " + this.getUuid());
            console.log("  Value: " + bytes2hex(value));
            console.log("  Service UUID: " + this.getService().getUuid());
            return this.setValue(value);
        };
        
        console.log("[+] BluetoothGattCharacteristic hooks installed");
    } catch (e) {
        console.log("[-] Failed to hook BluetoothGattCharacteristic: " + e);
    }
    
    // Hook BluetoothGatt operations
    try {
        var BluetoothGatt = Java.use("android.bluetooth.BluetoothGatt");
        
        // Hook readCharacteristic
        BluetoothGatt.readCharacteristic.implementation = function(characteristic) {
            console.log("[BLE] GATT Read Characteristic:");
            console.log("  Device: " + this.getDevice().getAddress());
            console.log("  Characteristic UUID: " + characteristic.getUuid());
            console.log("  Service UUID: " + characteristic.getService().getUuid());
            return this.readCharacteristic(characteristic);
        };
        
        // Hook writeCharacteristic
        BluetoothGatt.writeCharacteristic.implementation = function(characteristic) {
            console.log("[BLE] GATT Write Characteristic:");
            console.log("  Device: " + this.getDevice().getAddress());
            console.log("  Characteristic UUID: " + characteristic.getUuid());
            console.log("  Service UUID: " + characteristic.getService().getUuid());
            console.log("  Value: " + bytes2hex(characteristic.getValue()));
            return this.writeCharacteristic(characteristic);
        };
        
        // Hook setCharacteristicNotification
        BluetoothGatt.setCharacteristicNotification.implementation = function(characteristic, enable) {
            console.log("[BLE] GATT Set Notification:");
            console.log("  Device: " + this.getDevice().getAddress());
            console.log("  Characteristic UUID: " + characteristic.getUuid());
            console.log("  Enable: " + enable);
            return this.setCharacteristicNotification(characteristic, enable);
        };
        
        console.log("[+] BluetoothGatt hooks installed");
    } catch (e) {
        console.log("[-] Failed to hook BluetoothGatt: " + e);
    }
    
    // Hook Flutter Reactive BLE library
    try {
        var ReactiveBleClient = Java.use("com.signify.hue.flutterreactiveble.ble.ReactiveBleClient");
        
        // Hook readCharacteristic
        ReactiveBleClient.readCharacteristic.implementation = function(deviceId, characteristicUuid, serviceUuid) {
            console.log("[BLE] ReactiveBle Read:");
            console.log("  Device ID: " + deviceId);
            console.log("  Characteristic UUID: " + characteristicUuid);
            console.log("  Service UUID: " + serviceUuid);
            return this.readCharacteristic(deviceId, characteristicUuid, serviceUuid);
        };
        
        // Hook writeCharacteristicWithResponse
        ReactiveBleClient.writeCharacteristicWithResponse.implementation = function(deviceId, characteristicUuid, serviceUuid, data) {
            console.log("[BLE] ReactiveBle Write (with response):");
            console.log("  Device ID: " + deviceId);
            console.log("  Characteristic UUID: " + characteristicUuid);
            console.log("  Service UUID: " + serviceUuid);
            console.log("  Data: " + bytes2hex(data));
            return this.writeCharacteristicWithResponse(deviceId, characteristicUuid, serviceUuid, data);
        };
        
        // Hook writeCharacteristicWithoutResponse
        ReactiveBleClient.writeCharacteristicWithoutResponse.implementation = function(deviceId, characteristicUuid, serviceUuid, data) {
            console.log("[BLE] ReactiveBle Write (without response):");
            console.log("  Device ID: " + deviceId);
            console.log("  Characteristic UUID: " + characteristicUuid);
            console.log("  Service UUID: " + serviceUuid);
            console.log("  Data: " + bytes2hex(data));
            return this.writeCharacteristicWithoutResponse(deviceId, characteristicUuid, serviceUuid, data);
        };
        
        console.log("[+] ReactiveBleClient hooks installed");
    } catch (e) {
        console.log("[-] Failed to hook ReactiveBleClient: " + e);
    }
    
    // Hook device discovery
    try {
        var BluetoothAdapter = Java.use("android.bluetooth.BluetoothAdapter");
        
        // Hook startDiscovery
        BluetoothAdapter.startDiscovery.implementation = function() {
            console.log("[BLE] Starting device discovery...");
            return this.startDiscovery();
        };
        
        // Hook getRemoteDevice
        BluetoothAdapter.getRemoteDevice.implementation = function(address) {
            console.log("[BLE] Getting remote device: " + address);
            return this.getRemoteDevice(address);
        };
        
        console.log("[+] BluetoothAdapter hooks installed");
    } catch (e) {
        console.log("[-] Failed to hook BluetoothAdapter: " + e);
    }
    
    // Hook UUID creation
    try {
        var UUID = Java.use("java.util.UUID");
        
        UUID.fromString.implementation = function(uuidString) {
            console.log("[BLE] UUID Created: " + uuidString);
            return this.fromString(uuidString);
        };
        
        console.log("[+] UUID hooks installed");
    } catch (e) {
        console.log("[-] Failed to hook UUID: " + e);
    }
});

// Utility function to convert byte array to hex string
function bytes2hex(array) {
    if (!array) return "null";
    var result = "";
    for (var i = 0; i < array.length; i++) {
        result += ("0" + (array[i] & 0xFF).toString(16)).slice(-2);
    }
    return result;
}

// Hook onCharacteristicChanged callback
Java.perform(function() {
    try {
        var BluetoothGattCallback = Java.use("android.bluetooth.BluetoothGattCallback");
        
        BluetoothGattCallback.onCharacteristicChanged.implementation = function(gatt, characteristic) {
            console.log("[BLE] Characteristic Changed:");
            console.log("  Device: " + gatt.getDevice().getAddress());
            console.log("  Characteristic UUID: " + characteristic.getUuid());
            console.log("  Service UUID: " + characteristic.getService().getUuid());
            console.log("  Value: " + bytes2hex(characteristic.getValue()));
            return this.onCharacteristicChanged(gatt, characteristic);
        };
        
        console.log("[+] BluetoothGattCallback hooks installed");
    } catch (e) {
        console.log("[-] Failed to hook BluetoothGattCallback: " + e);
    }
});

console.log("[+] BLE hooks installation complete");
console.log("[+] Monitor the output for BLE communication patterns"); 