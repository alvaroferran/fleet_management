#!/usr/bin/env python3

import json
import os
from typing import Optional

import mongomock
from flask import Flask, request
from flask_pymongo import PyMongo  # type: ignore
from waitress import serve

from common.device import Device


def create_app(db_uri: Optional[str] = None) -> Flask:
    """Create Flask app to handle incoming requests and manage the database.

    Args:
        db_uri (Optional[str], optional): Mongo configuration string. Defaults to None.

    Returns:
        Flask: Configured app ready to be served.
    """
    app = Flask(__name__)

    # If URI is passed, connect to Mongo DB, otherwise create mock for testing.
    if db_uri:
        app.config["MONGO_URI"] = db_uri
        mongo = PyMongo(app)
        db = mongo.db.collection
    else:
        db = mongomock.MongoClient().db.collection

    @app.route("/devices/")
    def get_devices():
        devices = list(db.find({}))
        if devices:
            return json.dumps(devices), 200
        return "No devices found", 404

    @app.route("/devices/<int:device_id>")
    def get_device(device_id):
        device = db.find_one({"_id": device_id})
        if device:
            return json.dumps(device), 200
        return f"Device {device_id} not found", 404

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

    @app.route("/devices/<int:device_id>", methods=["DELETE"])
    def delete_device(device_id):
        if db.find_one({"_id": device_id}):
            db.delete_one({"_id": device_id})
            return f"Device {device_id} deleted successfully", 200
        else:
            return "", 204

    return app


if __name__ == "__main__":
    # Configure database
    with open(os.environ["MONGO_PASSWORD_FILE"], "r") as f_in:
        password = f_in.readline().rstrip()
    user = os.environ["MONGO_USERNAME"]
    host = os.environ["MONGO_HOSTNAME"]
    port = os.environ["MONGO_PORT"]
    db = os.environ["MONGO_DATABASE"]
    mongo_uri = f"mongodb://{user}:{password}@{host}:{port}/{db}"

    app = create_app(db_uri=mongo_uri)
    serve(app, host="0.0.0.0", port=os.environ["FLASK_PORT"])  # bind to any ip
