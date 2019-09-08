import time
import datetime
import Adafruit_DHT
# import Adafruit_CharLCD as LCD
import os
from influxdb import InfluxDBClient

host = "influxdb"
port = 8086
user = "rpi"
password = "rpi"
db_name = "sensor_data"
interval = int(os.getenv("INTERVAL", 60))
measurement = "rpi-dht22"
location = "living-room"

client = InfluxDBClient(host, port, user, password, db_name)

# Temp sensor
sensor = Adafruit_DHT.DHT22
sensor_gpio = 4

# LCD
lcd_rs        = 25
lcd_en        = 24
lcd_d4        = 23
lcd_d5        = 17
lcd_d6        = 18
lcd_d7        = 22
lcd_backlight = 4
lcd_columns = 16
lcd_rows    = 2
# lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7,
#                            lcd_columns, lcd_rows, lcd_backlight)


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
        # lcd.clear()
        # lcd.message("Temp:      %.1fC\nHumidity:  %.1f%%" % (temperature, humidity))
        time.sleep(interval)

except KeyboardInterrupt:
    pass

