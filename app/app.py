#!/usr/bin/env python3

import json

from flask import Flask, request
from flask_pymongo import PyMongo

from common.device import Device


app = Flask(__name__)

devices = []


@app.route("/devices/<int:device_id>")
def check_device(device_id):
    for device in devices:
        if device.device_id == device_id:
            return f"Device {device_id} found", 200
    return f"Device {device_id} not found", 404


@app.route("/devices/<int:device_id>", methods=["DELETE"])
def delete_device(device_id):
    for device in devices:
        if device.device_id == device_id:
            devices.remove(device)
            return f"Device {device_id} deleted successfully", 200
    else:
        return "", 204


@app.route("/devices/<int:device_id>", methods=["POST"])
def create_device(device_id):
    for device in devices:
        if device.device_id == device_id:
            return "", 204
    devices.append(Device(device_id=device_id))
    return f"Device {device_id} created successfully", 201


@app.route("/devices/<int:device_id>", methods=["PUT"])
def update_device(device_id):
    device_in = json.loads(request.get_json())
    for device in devices:
        if device.device_id == device_id:
            # Cast received values to field types before assignment
            for attr in list(device_in.keys()):
                if hasattr(device, attr):
                    attr_type = eval(f"type(Device.{attr})")
                    attr_val = attr_type(device_in[attr])
                    setattr(device, attr, attr_val)
            return f"Device {device_id} updated successfully", 200
    return f"Device {device_id} not found", 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5001")  # 0.0.0.0 to bind to any incoming ip
