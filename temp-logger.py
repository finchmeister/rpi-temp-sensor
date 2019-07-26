import time
import os
import datetime
import random
from influxdb import InfluxDBClient

# The sensor cannot be accessed through docker
# DOCKER mode is for testing with mock data
is_docker = "DOCKER" in os.environ

if is_docker is False:
    import Adafruit_DHT

host = "influxdb" if is_docker else "localhost"
port = 8086
user = "rpi"
password = "rpi"
db_name = "sensor_data"
interval = 5 if is_docker else 60
measurement = "rpi-dht22"
location = "living-room"

client = InfluxDBClient(host, port, user, password, db_name)

if is_docker:
    temperature = 25
    humidity = 52
else:
    sensor = Adafruit_DHT.DHT22
    sensor_gpio = 4

try:
    while True:

        if is_docker:
            temperature = temperature + random.uniform(-0.1, 0.1)
            humidity = humidity + random.uniform(-0.1, 0.1)
        else:
            humidity, temperature = Adafruit_DHT.read_retry(sensor, sensor_gpio)

        iso = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
        # print("[%s] Temp: %s, Humidity: %s" % (iso, temperature, humidity))
        data = [
            {
                "measurement": measurement,
                "tags": {
                    "location": location,
                },
                "time": iso,
                "fields": {
                    "temperature" : temperature,
                    "humidity": humidity
                }
            }
        ]
        client.write_points(data)
        time.sleep(interval)

except KeyboardInterrupt:
    pass
