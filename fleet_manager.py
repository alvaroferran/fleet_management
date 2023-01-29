#!/usr/bin/env python3

import json

from flask import Flask, request

from device import Device


app = Flask(__name__)

devices = []


@app.route("/check_device/")
def check_device():
    device_id = int(request.get_json())
    for device in devices:
        if device.device_id == device_id:
            return json.dumps(True), 200
    return json.dumps(False), 200


@app.route("/delete_device/", methods=["DELETE"])
def delete_device():
    device_id = int(request.get_json())
    for device in devices:
        if device.device_id == device_id:
            devices.remove(device)
            return f"Device {device_id} deleted successfully", 200
    else:
        return "", 204


@app.route("/create_device/", methods=["PUT", "POST"])
def create_device():
    device_id = int(request.get_json())
    for device in devices:
        if device.device_id == device_id:
            return "", 204
    devices.append(Device(device_id=device_id))
    return f"Device {device_id} created successfully", 200


@app.route("/update_device/", methods=["PUT", "POST"])
def update_device():
    device_in = json.loads(request.get_json())
    for device in devices:
        if device.device_id == int(device_in["device_id"]):
            # Cast received values to field types before assignment
            for attr in list(device_in.keys()):
                if attr == "device_id":
                    continue
                if hasattr(device, attr):
                    attr_type = eval(f"type(Device.{attr})")
                    attr_val = attr_type(device_in[attr])
                    setattr(device, attr, attr_val)
            return f"Device {device_in['device_id']} updated successfully", 200
    return "Device not found", 404


if __name__ == "__main__":
    app.run(host="localhost")
