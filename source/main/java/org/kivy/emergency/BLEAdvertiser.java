package org.kivy.emergency;

import android.bluetooth.BluetoothAdapter;
import android.bluetooth.le.AdvertiseCallback;
import android.bluetooth.le.AdvertiseData;
import android.bluetooth.le.AdvertiseSettings;
import android.bluetooth.le.BluetoothLeAdvertiser;
import android.content.Context;
import android.os.ParcelUuid;
import android.util.Log;

import java.io.File;
import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.UUID;

import java.io.BufferedWriter;
import java.io.FileWriter;


public class BLEAdvertiser {
    private static final String TAG = "BLEAdvertiser";
    private BluetoothLeAdvertiser bluetoothLeAdvertiser;
    private File receivedDataDir;

    public BLEAdvertiser(Context context) {
        BluetoothAdapter bluetoothAdapter = BluetoothAdapter.getDefaultAdapter();
        if (bluetoothAdapter != null && bluetoothAdapter.isEnabled()) {
            bluetoothLeAdvertiser = bluetoothAdapter.getBluetoothLeAdvertiser();
        } else {
            Log.e(TAG, "Bluetooth not supported or not enabled.");
        }

        receivedDataDir = new File(context.getFilesDir(), "Received_data");
        if (!receivedDataDir.exists()) {
            receivedDataDir.mkdirs();
        }
    }

    public void startAdvertising(String dictionaryEntry) {
        if (bluetoothLeAdvertiser == null) {
            Log.e(TAG, "BluetoothLeAdvertiser is not initialized.");
            return;
        }

        String serviceUuid = UUID.randomUUID().toString();

        AdvertiseSettings settings = new AdvertiseSettings.Builder()
                .setAdvertiseMode(AdvertiseSettings.ADVERTISE_MODE_LOW_LATENCY)
                .setConnectable(true)
                .setTimeout(0)
                .setTxPowerLevel(AdvertiseSettings.ADVERTISE_TX_POWER_HIGH)
                .build();

        AdvertiseData data = new AdvertiseData.Builder()
                .addServiceUuid(new ParcelUuid(UUID.fromString(serviceUuid)))
                .addServiceData(new ParcelUuid(UUID.fromString(serviceUuid)), dictionaryEntry.getBytes())
                .setIncludeDeviceName(true)
                .build();

        bluetoothLeAdvertiser.startAdvertising(settings, data, new AdvertiseCallback() {
            @Override
            public void onStartSuccess(AdvertiseSettings settingsInEffect) {
                Log.i(TAG, "Advertising started successfully.");
            }

            @Override
            public void onStartFailure(int errorCode) {
                Log.e(TAG, "Advertising failed with error code: " + errorCode);
            }
        });
    }

    public void saveReceivedData(String address, String data) {
        String dateDirectoryName = getCurrentDateDirectoryName();
        File dateDirectory = new File(receivedDataDir, dateDirectoryName);

        if (!dateDirectory.exists()) {
            dateDirectory.mkdirs();
        }

        File deviceFile = new File(dateDirectory, address + ".txt");

        try {
            if (!deviceFile.exists()) {
                deviceFile.createNewFile();
            }
            try (BufferedWriter writer = new BufferedWriter(new FileWriter(deviceFile, true))) {
                writer.write(data + "\n");  // Append data to the file
            } catch (IOException e) {
                Log.e(TAG, "Error appending data to file", e);
            }
        } catch (IOException e) {
            Log.e(TAG, "Failed to save received data", e);
        }
    }

    private String getCurrentDateDirectoryName() {
        SimpleDateFormat sdf = new SimpleDateFormat("MMMM_d_yyyy");
        return sdf.format(new Date());
    }
}