# Fleet management
API to manage a fleet of distributed devices.


## Build
Set the database user and admin passwords. Eg.

    echo "very_long_but_easy_to_remember_user_password" > mongo/secrets/mongo_password.txt
    echo "very_long_but_easy_to_remember_admin_password" > mongo/secrets/mongo_root_password.txt

To build the images run

    docker compose build


## Run

Execute the fleet management system:

    docker compose run server

and then the test client:

    docker compose run --rm test_client
