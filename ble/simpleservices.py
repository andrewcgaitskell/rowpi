from bluepy import btle

from bluepy.btle import UUID, Peripheral, DefaultDelegate


print("Connecting...")
dev = btle.Peripheral("FA:D0:B8:89:AE:1F", btle.ADDR_TYPE_RANDOM)

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
