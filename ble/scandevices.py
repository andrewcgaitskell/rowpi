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
            self.svcs = self.discoverServices();
        
        #fwVers = self.getCharacteristics(uuid=AssignedNumbers.firmwareRevisionString)
        
        #if len(fwVers) >= 1:
        #    self.firmwareVersion = fwVers[0].read().decode("utf-8")
        #else:
        #    self.firmwareVersion = u''
        
        self.characteristics = self.getCharacteristics()
        
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
    
    if (dev.addr == 'b0:b4:48:bd:7a:87' or dev.addr == '6b:81:79:16:93:1f' or dev.addr == '30:ae:a4:83:f9:46'):
        #try:
        ldev = LocalBLEDevice(dev.addr);
        l_dict = ldev.svcs;
        d_items = l_dict.items();
        for key, value in d_items:
            try:
                local_uuid = key.getCommonName()
            except:
                local_uuid = ''
            print("local_uuid -> ", local_uuid, " value ->" , value);
        #except:
        #    a = 1;
        c_list = ldev.characteristics;
        
        for l in c_list:
            try:
                print("characteristic list -> ",l)
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
        
