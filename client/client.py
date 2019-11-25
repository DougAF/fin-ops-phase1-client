import re
import uuid
from bluepy.btle import Scanner

def get_mac():
    mac = hex(uuid.getnode())
    return ":".join([mac[i : i + 2] for i in range(2, len(mac), 2)]).replace("x", "0") 

print(get_mac())

scanner = Scanner()

while True:
    devices = scanner.scan(1)
    for device in devices:
        print("DEV = {} RSSI = {}".format(device.addr, device.rssi))

