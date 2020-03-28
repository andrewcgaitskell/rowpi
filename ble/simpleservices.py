from bluepy import btle

from bluepy.btle import UUID, Peripheral, DefaultDelegate


print("Connecting...")
# test beacon 30:ae:a4:83:f9:46

#dev = btle.Peripheral("FA:D0:B8:89:AE:1F", btle.ADDR_TYPE_RANDOM) # cadence meter

dev = btle.Peripheral("30:AE:A4:83:F6:46", btle.ADDR_TYPE_PUBLIC) # test beacon

characteristicslist = dev.getCharacteristics()

CSC_SERVICE_UUID = UUID(0x1816)
CSC_CHAR_UUID = UUID(0x2A5B)
LOCATION_CHAR_UUID = UUID(0x2A5D)

print("Services...")
for svc in dev.services:
    print(str(svc))

print("Characteristics...")
for cl in characteristicslist:
    print(str(cl))
