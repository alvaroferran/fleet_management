FROM python:3.11

WORKDIR /test_client

# Install any dependencies
COPY ./common /test_client/common
RUN pip install -r common/requirements.txt

COPY ./test_client/test_client.py /test_client/

# Set the directive to specify the executable that will run when the container is initiated
ENTRYPOINT ["python", "test_client.py"]
