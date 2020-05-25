#! /usr/bin/python
import Adafruit_DHT
import Adafruit_CharLCD as LCD
import time

sensor = Adafruit_DHT.DHT22
sensor_gpio = 4

lcd_rs        = 25
lcd_en        = 24
lcd_d4        = 23
lcd_d5        = 17
lcd_d6        = 18
lcd_d7        = 22
lcd_backlight = 15

lcd_columns = 16
lcd_rows    = 2

# Initialize the LCD using the pins above.
lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7,
                           lcd_columns, lcd_rows, lcd_backlight, False)

lcd.set_backlight(0)

humidity, temperature = Adafruit_DHT.read_retry(sensor, sensor_gpio)
if humidity is None or temperature is None:
    quit()
lcd.clear()
lcd.message("Temp:      %.1fC\nHumidity:  %.1f%%" % (temperature, humidity))
quit()

# Legacy long running version below:
try:
    while True:
        humidity, temperature = Adafruit_DHT.read_retry(sensor, sensor_gpio)
        if humidity is None or temperature is None:
            continue
        lcd.clear()
        lcd.message("Temp:      %.1fC\nHumidity:  %.1f%%" % (temperature, humidity))
        time.sleep(160)

except KeyboardInterrupt:
    pass
