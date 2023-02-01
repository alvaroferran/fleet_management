#!/usr/bin/env python3

import json
import os

from flask import Flask, request
from flask_pymongo import PyMongo
from waitress import serve

from common.device import Device


with open(os.environ["MONGO_PASSWORD_FILE"], "r") as f_in:
    mongo_pwd = f_in.readline().rstrip()

app = Flask(__name__)
app.config["MONGO_URI"] = (
    f"mongodb://{os.environ['MONGO_USERNAME']}:{mongo_pwd}"
    + f"@{os.environ['MONGO_HOSTNAME']}:27017/{os.environ['MONGO_DATABASE']}"
)

mongo = PyMongo(app)
db = mongo.db.coll


@app.route("/devices/<int:device_id>")
def check_device(device_id):
    if db.find_one({"_id": device_id}):
        return f"Device {device_id} found", 200
    return f"Device {device_id} not found", 404


@app.route("/devices/<int:device_id>", methods=["DELETE"])
def delete_device(device_id):
    if db.find_one({"_id": device_id}):
        db.delete_one({"_id": device_id})
        return f"Device {device_id} deleted successfully", 200
    else:
        return "", 204


@app.route("/devices/<int:device_id>", methods=["POST"])
def create_device(device_id):
    if db.find_one({"_id": device_id}):
        return "", 204
    else:
        db.insert_one(Device(_id=device_id).__dict__)
        return f"Device {device_id} created successfully", 201


@app.route("/devices/<int:device_id>", methods=["PUT"])
def update_device(device_id):
    device = db.find_one({"_id": device_id})
    if device:
        device_in = json.loads(request.get_json())
        # Only allow updating fields present in Device
        device_fields = list(device.keys())
        for key in list(device_in.keys()):
            if key in device_fields:
                if key == "_id":  # Do not update ID field
                    continue
                device[key] = device_in[key]
        db.update_one({"_id": device_id}, {"$set": device})
        return f"Device {device_id} updated successfully", 200
    return f"Device {device_id} not found", 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5001")  # 0.0.0.0 to bind to any ip
    # serve(app, host="0.0.0.0", port="5001")  # 0.0.0.0 to bind to any ip
