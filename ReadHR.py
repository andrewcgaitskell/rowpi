# This code is intended to run on a device with up to date Bluez.
# Works on Raspberry Pi or Mac.
# Currently configured to stream heart rate.
# https://www.bluetooth.com/specifications/gatt/viewer?attributeXmlFile=org.bluetooth.service.heart_rate.xml
# Bluepy Docs
# @see http://ianharvey.github.io/bluepy-doc/
#  Notifciations doc: 
# @see http://ianharvey.github.io/bluepy-doc/notifications.html
# Code assumes adapter is already enabled, and scan was already done.

from bluepy import btle
import time
import binascii

# Address of BLE device to connect to.
BLE_ADDRESS = "00:22:D0:2A:7F:99" # changed this to my own
# BLE heart rate service
BLE_SERVICE_UUID ="A1D1BB46-AA06-CA32-ABAE-DE11DFF9C688"
# Heart rate measurement that notifies.
BLE_CHARACTERISTIC_UUID= "00001800-0000-1000-8000-00805f9b34fb";


class MyDelegate(btle.DefaultDelegate):
    def __init__(self):
        btle.DefaultDelegate.__init__(self)
        # ... initialise here

    def handleNotification(self, cHandle, data):
    	data = bytearray(data)
    	print 'Developer: do what you want with the data.'
    	print data



print "Connecting..."
dev = btle.Peripheral(BLE_ADDRESS)
dev.setDelegate( MyDelegate() )
 
service_uuid = btle.UUID(BLE_SERVICE_UUID)
ble_service = dev.getServiceByUUID(service_uuid)

uuidConfig = btle.UUID(BLE_CHARACTERISTIC_UUID)
data_chrc = ble_service.getCharacteristics(uuidConfig)[0]

# print "Debug Services..."
# for svc in dev.services:
# 	print str(svc)

# print 'Debug Characteristics...'
# for ch in es_service.getCharacteristics():
# 	print str(ch)

# Enable the sensor, start notifications
# Writing x01 is the protocol for all BLE notifications.
data_chrc.write(bytes("\x01")) 

time.sleep(1.0) # Allow sensor to stabilise


# Main loop --------
while True:
    if dev.waitForNotifications(1.0):
        # handleNotification() was called
        continue
    print "Waiting..."
