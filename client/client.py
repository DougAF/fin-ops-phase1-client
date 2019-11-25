import subprocess
import re
import uuid
from bluepy.btle import Scanner

def get_mac():
    mac = hex(uuid.getnode())
    return ":".join([mac[i : i + 2] for i in range(2, len(mac), 2)]).replace("x", "0")

def get_ble_mac():
    cmd = "hcitool dev"
    result = subprocess.run(["hcitool", "dev"], capture_output=True)
    out = result.stdout
    mac_regex = re.compile(r"[0-9a-f]{2}(:[0-9a-f]{2}){5}", re.IGNORECASE)
    mac = mac_regex.search(out.decode("utf-8")).group()
    return mac.lower()

scanner = Scanner()
 
print(get_mac())
print(get_ble_mac())

scanner = Scanner()

while True:
    devices = scanner.scan(1)
    for device in devices:
        print("DEV = {} RSSI = {}".format(device.addr, device.rssi))

