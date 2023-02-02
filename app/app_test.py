import json

import flask_unittest  # type: ignore

from app.app import create_app
from common.device import Device


class TestClass(flask_unittest.ClientTestCase):
    app = create_app()

    def test_1_create_device(self, client):
        device_id = 1000
        # Database is empty when initialized, device should not exist
        found = client.get(f"/devices/{device_id}")
        self.assertEqual(found.status_code, 404)
        # Create device
        create = client.post(f"/devices/{device_id}")
        self.assertEqual(create.status_code, 201)
        # Check device now exists
        found = client.get(f"/devices/{device_id}")
        self.assertEqual(found.status_code, 200)

    def test_2_create_device_again(self, client):
        device_id = 1000
        create = client.post(f"/devices/{device_id}")
        self.assertEqual(create.status_code, 204)

    def test_3_get_devices(self, client):
        found = client.get("/devices/")
        expected = (
            '[{"_id": 1000, "alias": "", "client": "", "payment_required": true}]'
        )
        self.assertEqual(found.status_code, 200)
        self.assertEqual(found.data.decode("utf-8"), expected)

    def test_4_update_device_pass(self, client):
        device_id = 1000
        # Retrieve existing device
        found = client.get(f"/devices/{device_id}")
        expected_old = (
            '{"_id": 1000, "alias": "", "client": "", "payment_required": true}'
        )
        self.assertEqual(found.status_code, 200)
        self.assertEqual(found.data.decode("utf-8"), expected_old)
        # Update device
        device = Device(_id=device_id)
        device.alias = f"Test device {device_id}"
        device.payment_required = False
        device_json = json.dumps(device.__dict__)
        updated = client.put(f"/devices/{device_id}", json=device_json)
        self.assertEqual(updated.status_code, 200)
        # Retrieve device again
        found = client.get(f"/devices/{device_id}")
        expected_new = (
            '{"_id": 1000, "alias": "Test device 1000", "client": "",'
            + ' "payment_required": false}'
        )
        self.assertEqual(found.status_code, 200)
        self.assertNotEqual(found.data.decode("utf-8"), expected_old)
        self.assertEqual(found.data.decode("utf-8"), expected_new)

    def test_5_update_device_fail(self, client):
        device_id = 2000
        # Retrieve non-existing device
        found = client.get(f"/devices/{device_id}")
        self.assertEqual(found.status_code, 404)
        # Update device
        device = Device(_id=device_id)
        device.alias = f"Test device {device_id}"
        device.payment_required = False
        device_json = json.dumps(device.__dict__)
        updated = client.put(f"/devices/{device_id}", json=device_json)
        self.assertEqual(updated.status_code, 404)

    def test_6_delete_device(self, client):
        device_id = 1000
        # Check device exists
        found = client.get(f"/devices/{device_id}")
        self.assertEqual(found.status_code, 200)
        # Delete device
        deleted = client.delete(f"/devices/{device_id}")
        self.assertEqual(deleted.status_code, 200)
        # Check device no longer exists
        found = client.get(f"/devices/{device_id}")
        self.assertEqual(found.status_code, 404)

    def test_7_delete_device_again(self, client):
        device_id = 1000
        deleted = client.delete(f"/devices/{device_id}")
        self.assertEqual(deleted.status_code, 204)

    def test_8_get_devices_again(self, client):
        found = client.get("/devices/")
        self.assertEqual(found.status_code, 404)
        self.assertEqual(found.data.decode("utf-8"), "No devices found")
