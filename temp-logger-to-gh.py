import datetime
import json
import Adafruit_DHT
import os
import sys

measurement = "rpi-dht22"
location = "bedroom"

# Temp sensor
sensor = Adafruit_DHT.DHT22
sensor_gpio = 4

humidity, temperature = Adafruit_DHT.read_retry(sensor, sensor_gpio)
iso = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
if humidity is None or temperature is None:
    sys.exit("[%s] There was an error fetching the temperature data" % iso)

humidity = round(humidity, 2)
temperature = round(temperature, 2)
print("[%s] Temp: %s, Humidity: %s" % (iso, temperature, humidity))

data = [
    {
        "measurement": measurement,
        "tags": {
            "location": location,
        },
        "time": iso,
        "fields": {
            "temperature": temperature,
            "humidity": humidity
        }
    }
]
f = open("/home/pi/bedroom-temperature-api/temperature.json", "w")
f.write(json.dumps(data[0], sort_keys=True, indent=4))
f.close()
os.system("cd /home/pi/bedroom-temperature-api && "
          "git add temperature.json "
          "&& git commit -m '" + iso + "' "
          "&& git push origin master")
