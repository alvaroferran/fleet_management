#!/usr/bin/env python3

import json
import random

import requests


def main():
    ip = "http://localhost:5001"
    device_ids = [112, 358, 132, 134]

    # Check if random device exists in fleet
    device_id = random.choice(device_ids)
    print(f"Checking if device {device_id} exists.")
    device_exists = requests.get(f"{ip}/devices/{device_id}").json()

    if device_exists:
        # If device exists, delete it from database
        print(f"Device {device_id} exists, requesting deletion.")
        ret = requests.delete(f"{ip}/devices/{device_id}")
        print(ret.text)
    else:
        # Create device
        print(f"Device {device_id} doesn't exist, creating.")
        ret = requests.put(f"{ip}/devices/{device_id}")
        print(ret.text)
        if ret.ok:
            # Update device
            device = {
                "alias": f"Test device {device_id}",
                "payment_required": False,
            }
            device = json.dumps(device)
            ret = requests.post(f"{ip}/devices/{device_id}", json=device)
            print(ret.text)


if __name__ == "__main__":
    main()
