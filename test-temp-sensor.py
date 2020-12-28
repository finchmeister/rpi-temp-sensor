import Adafruit_DHT

sensor = Adafruit_DHT.DHT22
sensor_gpio = 4

humidity, temperature = Adafruit_DHT.read_retry(sensor, sensor_gpio)
print("Temp: %.2f, Humidity: %.2f" % (temperature, humidity))