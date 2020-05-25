import time
import datetime
import json
import Adafruit_DHT
import os

interval = int(os.getenv("INTERVAL", 120))
measurement = "rpi-dht22"
location = "bedroom"

# Temp sensor
sensor = Adafruit_DHT.DHT22
sensor_gpio = 4

try:
    while True:
        humidity, temperature = Adafruit_DHT.read_retry(sensor, sensor_gpio)
        # humidity = 0.7
        # temperature = 15
        iso = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
        print("[%s] Temp: %s, Humidity: %s" % (iso, temperature, humidity))
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
        f = open("/home/pi/bedroom-temperature-api/temperature.json", "w")
        f.write(json.dumps(data[0], sort_keys=True, indent=4))
        f.close()
        os.system("cd /home/pi/bedroom-temperature-api && "
                  "git add temperature.json "
                  "&& git commit -m '" + iso + "' "
                  "&& git push origin master")

        time.sleep(interval)

except KeyboardInterrupt:
    pass

