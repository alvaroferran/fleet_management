FROM python:3.11

WORKDIR /app

COPY ./common /app/common
COPY ./app/ /app/
RUN pip install -r requirements.txt

ENTRYPOINT ["python", "app.py"]
