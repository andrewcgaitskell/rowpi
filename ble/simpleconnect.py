from bluepy import btle
from bluepy.btle import Scanner, DefaultDelegate

def runScanAndSet():
    global found;
    found = False;
    devices = scanner.scan(3)
    try:
        peripheral = btle.Peripheral('fa:d0:b8:89:ae:1f', btle.ADDR_TYPE_RANDOM)
        failures = 0;
    except:
        print('failed to connect')

def main():
    """ Main program """
    # Code goes over here.
    runScanAndSet();
    return 0

if __name__ == "__main__":
    main()
