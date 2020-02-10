import requests
import json
import datetime
import subprocess
import re
import uuid
from bluepy.btle import Scanner


HEADERS = {"Content-Type": "application/json"}

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

def get_time():
    return datetime.datetime.utcnow().isoformat()

if __name__ == "__main__":
    import sys

    try:
        server_ip = sys.argv[1].strip()
    except:
        raise Exception(
            "Must include the server's ip. Example: python mock_post.py 127.0.0.1 \n"
            "If the port running the app is not the default (80), must include the port. \n"
            "Example: python mock_post.py 127.0.0.1:5000 "
        )

    scanner = Scanner()

    while True:
        devices = scanner.scan(0.005)
        for device in devices:
            data = {
                "recorder_time": get_time(),
                "recorder_mac": get_mac(),
                "recorder_ble_mac": get_ble_mac(),
                "transmitter_ble_mac": device.addr,
                "rssi": device.rssi,
            }
        
        try:
            r = requests.post(f"http://{server_ip}/collect", json=json.dumps(data))
            print(f"response code: {r.status_code}")
            print(f"response: {r.text}")
        except:
            print("Could not reach server.")
