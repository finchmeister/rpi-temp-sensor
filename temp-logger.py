import time
import datetime
import Adafruit_DHT
from influxdb import InfluxDBClient

host = "influxdb"
port = 8086
user = "rpi"
password = "rpi"
db_name = "sensor_data"
interval = 60
measurement = "rpi-dht22"
location = "living-room"

client = InfluxDBClient(host, port, user, password, db_name)

sensor = Adafruit_DHT.DHT22
sensor_gpio = 4

try:
    while True:
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
