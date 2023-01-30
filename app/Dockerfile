FROM python:3.11

WORKDIR /app

# Install any dependencies
COPY ./common /app/common
RUN pip install -r common/requirements.txt

COPY ./app/app.py /app/

# Set the directive to specify the executable that will run when the container is initiated
ENTRYPOINT ["python", "app.py"]
