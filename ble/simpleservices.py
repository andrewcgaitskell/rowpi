from bluepy import btle
 
print("Connecting...")
dev = btle.Peripheral("FA:D0:B8:89:AE:1F", btle.ADDR_TYPE_RANDOM)

characteristicslist = dev.getCharacteristics()


print("Services...")
for svc in dev.services:
    print(str(svc))

print("Characteristics...")
for cl in characteristicslist:
    print(str(cl))
