# Fleet management
Flask app with a REST API to manage a fleet of distributed devices.

## REST API

-  **Get list of devices:** &nbsp; `GET /devices/`

   - **Pass:**
     - Returns: List of found devices.
     - Status: 200
   - **Fail:**
     - Returns: "No devices found"
     - Status: 404

-  **Get device properties:** &nbsp; `GET /devices/<int:id>`
    - **Pass:**
        - Returns: Found device.
        - Status: 200
    - **Fail:**
        - Returns: "Device {device_id} not found"
        - Status: 404

-  **Create device:** &nbsp; `POST /devices/<int:id>`
    - **Pass:**
        - Returns: "Device {device_id} created successfully"
        - Status: 201
    - **Pass (device already exists):**
        - Returns: ""
        - Status: 204

-  **Update device:** &nbsp; `PUT /devices/<int:id>`
    - **Pass:**
        - Returns: "Device {device_id} updated successfully"
        - Status: 200
    - **Fail:**
        - Returns: "Device {device_id} not found"
        - Status: 404

-  **Remove device:** &nbsp; `DELETE /devices/<int:id>`
    - **Pass:**
        - Returns: "Device {device_id} deleted successfully"
        - Status: 200
    - **Pass (device doesn't exist):**
        - Returns: ""
        - Status: 204



## BUILD
Set the database user and admin passwords, eg.

    echo "very_long_but_easy_to_remember_user_password" > app/mongo/secrets/mongo_password.txt
    echo "very_long_but_easy_to_remember_admin_password" > app/mongo/secrets/mongo_root_password.txt

To build the images run

    docker compose build


## RUN

Execute the fleet management system:

    docker compose run -d server

and then the test client:

    docker compose run --rm test_client


## UNIT TEST

The server unit test can be used to verify the API endpoints with an ephemeral database.

    python3 -m unittest app.app_test
