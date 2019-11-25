from bluepy.btle import Scanner
 
scanner = Scanner()

while True:
    devices = scanner.scan(1)
    for device in devices:
        print("DEV = {} RSSI = {}".format(device.addr, device.rssi))

