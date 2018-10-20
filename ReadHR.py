# This code is intended to run on a device with up to date Bluez.
# Works on Raspberry Pi or Mac.
# Currently configured to stream heart rate.
# https://www.bluetooth.com/specifications/gatt/viewer?attributeXmlFile=org.bluetooth.service.heart_rate.xml
# Bluepy Docs
# @see http://ianharvey.github.io/bluepy-doc/
#  Notifciations doc: 
# @see http://ianharvey.github.io/bluepy-doc/notifications.html
# Code assumes adapter is already enabled, and scan was already done.

import sys
from bluepy import btle
from bluepy.btle import UUID, Peripheral
import time
import binascii

import struct

# Address of BLE device to connect to.
BLE_ADDRESS = "00:22:D0:2A:7F:99" # changed this to my own
# BLE heart rate service - 180d
BLE_SERVICE_UUID ="0000180d-0000-1000-8000-00805f9b34fb"
# Heart rate measurement that notifies - 2a37
BLE_CHARACTERISTIC_UUID= "00002a37-0000-1000-8000-00805f9b34fb";


p = Peripheral(BLE_ADDRESS)

services=p.getServices()

#displays all services
for service in services:
   print service

   
chList = p.getCharacteristics()
print "Handle   UUID                                Properties"
print "-------------------------------------------------------"                       
for ch in chList:
   print ("  0x"+ format(ch.getHandle(),'02X')  +"   "+str(ch.uuid) +" " + ch.propertiesToString())
   
   

#heart_service_uuid = UUID(0x000f)
rate_service_uuid    = UUID(0x11)

HeartService=p.getServiceByUUID(BLE_SERVICE_UUID)

try:
   ch = HeartService.getCharacteristics(BLE_CHARACTERISTIC_UUID)
   while 1:
      #val = binascii.b2a_hex(ch.read())
      #print ("0x" + val)
      h = ch.read()
      print(h)
      time.sleep(1)

finally:
    p.disconnect()
