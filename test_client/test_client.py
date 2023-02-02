#!/usr/bin/env python3

import json
import os
import random

import requests

from common.device import Device


def main(device_ids: list, ip: str):
    # Check if random device exists in fleet
    device_id = random.choice(device_ids)
    ret = requests.get(f"{ip}/devices/{device_id}")
    if ret.ok:
        print(f"Device {device_id} found: {ret.text}")
        # If device exists, delete it from database
        ret = requests.delete(f"{ip}/devices/{device_id}")
        print(ret.text)
    else:
        print(ret.text)
        # Create device
        ret = requests.post(f"{ip}/devices/{device_id}")
        print(ret.text)
        if ret.ok:
            # Update device
            device = Device(_id=device_id)
            device.alias = f"Test device {device_id}"
            device.payment_required = False
            device_json = json.dumps(device.__dict__)
            ret = requests.put(f"{ip}/devices/{device_id}", json=device_json)
            print(ret.text)


if __name__ == "__main__":
    main(
        device_ids=os.environ["DEVICE_IDS"].split(","),
        ip=f"http://localhost:{os.environ['FLASK_PORT']}",
    )
