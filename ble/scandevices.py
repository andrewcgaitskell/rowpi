#https://ianharvey.github.io/bluepy-doc/scanner.html
    
from bluepy.btle import Scanner, DefaultDelegate

from bluepy.btle import UUID, Peripheral, AssignedNumbers
import struct
import math
# Sensortag versions
AUTODETECT = "-"

class LocalBLEDevice(Peripheral):
    def __init__(self,addr,version=AUTODETECT):
        Peripheral.__init__(self,addr)
        if version==AUTODETECT:
            svcs = self.discoverServices();
        fwVers = self.getCharacteristics(uuid=AssignedNumbers.firmwareRevisionString)
        if len(fwVers) >= 1:
            self.firmwareVersion = fwVers[0].read().decode("utf-8")
        else:
            self.firmwareVersion = u''
        
class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            print("Discovered device", dev.addr)
        elif isNewData:
            print("Received new data from", dev.addr)

scanner = Scanner().withDelegate(ScanDelegate())
devices = scanner.scan(10.0)

for dev in devices:
    print("Device %s (%s), RSSI=%d dB" % (dev.addr, dev.addrType, dev.rssi))
    try:
        ldev = LocalBLEDevice(dev.addr)
    except:
        a = 1;
    for (adtype, desc, value) in dev.getScanData():
        print("  %s = %s" % (desc, value))

#print("new code")
        
#for dev in devices:
#    print("Device %s (%s), RSSI=%d dB" % (dev.addr, dev.addrType, dev.rssi))
#    dev_adtype = dev.addrType
#    
#    gd = dev.getDescription(dev_adtype)
#    print("gd",gd)
#    
#    gsd = dev.getScanData()
#    for (adtype, desc, value) in gsd:
#        print("  %s = %s" % (desc, value))
        
