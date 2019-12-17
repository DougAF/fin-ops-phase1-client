import uuid
import datetime
import random
import requests
import json
import time

HEADERS = {"Content-Type": "application/json"}
MOCK_LABELS = ["couch", "computer", "bunker", "basement", "closet", "kitchen"]

def get_time():
    return datetime.datetime.utcnow().isoformat()

def make_mock_data(mock_labels):
    return {
        "recorder_time": get_time(),
        "label": random.choice(mock_labels)
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

    while True:

        try:
            mock_data = make_mock_data(MOCK_LABELS)
            print(mock_data)
            r = requests.post(f"http://{server_ip}/collect_label", json=json.dumps(mock_data))
            print(f"response code: {r.status_code}")
            print(f"response: {r.text}")
        except:
            print("Could not reach server.")

        time.sleep(5)
