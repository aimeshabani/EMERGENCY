package org.kivy.emergency;

import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.bluetooth.BluetoothGatt;
import android.bluetooth.BluetoothGattCallback;
import android.bluetooth.BluetoothGattCharacteristic;
import android.bluetooth.BluetoothGattService;
import android.bluetooth.le.BluetoothLeScanner;
import android.bluetooth.le.ScanCallback;
import android.bluetooth.le.ScanResult;
import android.content.Context;
import android.util.Log;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.io.BufferedWriter;
import java.io.FileWriter;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.List;

public class BLEService {

    private static final String TAG = "BLEService";
    private BluetoothAdapter bluetoothAdapter;
    private BluetoothLeScanner bluetoothLeScanner;
    private Context context;
    private File serviceDirectory;
    private File receivedDataDir;

    private BluetoothGatt bluetoothGatt;
    private BluetoothGattCharacteristic writeCharacteristic;

    public BLEService(Context context) {
        this.context = context;
        this.bluetoothAdapter = BluetoothAdapter.getDefaultAdapter();
        this.bluetoothLeScanner = bluetoothAdapter.getBluetoothLeScanner();

        serviceDirectory = new File(context.getFilesDir(), "service");
        if (!serviceDirectory.exists()) {
            serviceDirectory.mkdirs();
        }

        receivedDataDir = new File(context.getFilesDir(), "Received_data");
        if (!receivedDataDir.exists()) {
            receivedDataDir.mkdirs();
        }
    }

    public void startScanning() {
        if (bluetoothAdapter != null && bluetoothAdapter.isEnabled()) {
            bluetoothLeScanner.startScan(new ScanCallback() {
                @Override
                public void onScanResult(int callbackType, ScanResult result) {
                    BluetoothDevice device = result.getDevice();
                    Log.i(TAG, "Discovered device: " + device.getAddress());
                    connectToDevice(device);
                }

                @Override
                public void onScanFailed(int errorCode) {
                    Log.e(TAG, "Scan failed with error code: " + errorCode);
                }
            });
        } else {
            Log.e(TAG, "Bluetooth is not enabled or unavailable");
        }
    }

    private void connectToDevice(BluetoothDevice device) {
        bluetoothGatt = device.connectGatt(context, false, gattCallback);
    }

    private final BluetoothGattCallback gattCallback = new BluetoothGattCallback() {
        @Override
        public void onConnectionStateChange(BluetoothGatt gatt, int status, int newState) {
            if (newState == BluetoothGatt.STATE_CONNECTED) {
                Log.i(TAG, "Connected to GATT server.");
                gatt.discoverServices();
            } else if (newState == BluetoothGatt.STATE_DISCONNECTED) {
                Log.i(TAG, "Disconnected from GATT server.");
                bluetoothGatt = null;
            }
        }

        @Override
        public void onServicesDiscovered(BluetoothGatt gatt, int status) {
            if (status == BluetoothGatt.GATT_SUCCESS) {
                for (BluetoothGattService service : gatt.getServices()) {
                    for (BluetoothGattCharacteristic characteristic : service.getCharacteristics()) {
                        writeCharacteristic = characteristic;
                        sendDictionaryToDevice();
                        readDictionaryFromDevice();
                    }
                }
            }
        }
    };

    private void sendDictionaryToDevice() {
        if (writeCharacteristic != null) {
            File[] files = serviceDirectory.listFiles();
            if (files != null && files.length > 0) {
                for (File file : files) {
                    try (BufferedReader reader = new BufferedReader(new FileReader(file))) {
                        String line;
                        while ((line = reader.readLine()) != null) {
                            writeCharacteristic.setValue(line.getBytes());
                            bluetoothGatt.writeCharacteristic(writeCharacteristic);
                            Log.i(TAG, "Sent dictionary entry: " + line);
                        }
                    } catch (IOException e) {
                        Log.e(TAG, "Error reading service directory file", e);
                    }
                }
            }
        }
    }

    private void readDictionaryFromDevice() {
        // Placeholder for receiving data; implement specific logic as needed
        // Any received data can be logged and stored similarly to the `receiveData` function
    }

    public void receiveData(String address, String data) {
        String dateDirectoryName = getCurrentDateDirectoryName();
        File dateDirectory = new File(receivedDataDir, dateDirectoryName);

        if (!dateDirectory.exists()) {
            dateDirectory.mkdirs();
        }

        File deviceFile = new File(dateDirectory, address + ".txt");

        try (BufferedWriter writer = new BufferedWriter(new FileWriter(deviceFile, true))) {
            writer.write(data);
            writer.newLine();
        } catch (IOException e) {
            Log.e(TAG, "Error writing received data to file", e);
        }
    }

    private String getCurrentDateDirectoryName() {
        SimpleDateFormat sdf = new SimpleDateFormat("MMMM_d_yyyy");
        return sdf.format(new Date());
    }
}