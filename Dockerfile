FROM python:2.7

WORKDIR /app

RUN pip install influxdb

COPY . .

CMD [ "python", "./temp-logger.py" ]