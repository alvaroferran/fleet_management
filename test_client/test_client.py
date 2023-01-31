#!/usr/bin/env python3

import json
import random

import requests

from common.device import Device


def main():
    ip = "http://localhost:5001"
    device_ids = [112, 358, 132, 134]

    # Check if random device exists in fleet
    device_id = random.choice(device_ids)
    ret = requests.get(f"{ip}/devices/{device_id}")
    print(ret.text)
    if ret.ok:
        # If device exists, delete it from database
        ret = requests.delete(f"{ip}/devices/{device_id}")
        print(ret.text)
    else:
        # Create device
        ret = requests.post(f"{ip}/devices/{device_id}")
        print(ret.text)
        if ret.ok:
            # Update device
            device = Device(device_id=device_id)
            device.alias = f"Test device {device_id}"
            device.payment_required = False
            device = json.dumps(device.__dict__)
            ret = requests.put(f"{ip}/devices/{device_id}", json=device)
            print(ret.text)


if __name__ == "__main__":
    main()
