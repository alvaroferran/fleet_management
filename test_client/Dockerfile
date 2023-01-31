FROM python:3.11

WORKDIR /test_client

COPY ./common /test_client/common
COPY ./test_client/ /test_client/
RUN pip install -r requirements.txt

ENTRYPOINT ["python", "test_client.py"]
