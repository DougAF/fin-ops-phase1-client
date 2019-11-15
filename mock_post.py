import uuid
import datetime
import random
import requests
import json
import time

HEADERS = {"Content-Type": "application/json"}


def get_mac():
    mac = hex(uuid.getnode())
    return ":".join([mac[i : i + 2] for i in range(2, len(mac), 2)]).replace("x", "0")


def get_time():
    return str(datetime.datetime.utcnow())


def make_mock_mac():

    mock_mac = ""

    for i in range(0, 6):
        mock_mac += hex(random.randint(0, 16))[-1]
        mock_mac += hex(random.randint(0, 16))[-1]
        mock_mac += ":"

    return mock_mac[0:-1]


def make_mock_data(mock_macs):
    return {
        "recorder_time": get_time(),
        "recorder_mac": get_mac(),
        "transmitter_mac": mock_macs[random.randint(0, len(mock_macs) - 1)],
        "rssi": random.randint(0, 10),
    }


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

    mock_macs = [make_mock_mac() for _ in range(0, 6)]

    while True:

        try:
            mock_data = make_mock_data(mock_macs)
            r = requests.post(f"http://{server_ip}/collect", json=json.dumps(mock_data))
            print(f"response code: {r.status_code}")
            print(f"response: {r.text}")
        except:
            print("Could not reach server.")

        time.sleep(5)
