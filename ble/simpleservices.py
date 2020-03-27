from bluepy import btle
 
print("Connecting...")
dev = btle.Peripheral("FA:D0:B8:89:AE:1F")

print("Services...")
for svc in dev.services:
    print(str(svc))
