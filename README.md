# Raspberry Pi Home Temperature Monitoring System


Requirements

- Raspberry Pi
- DHT22 temperature & humidity sensor

## Rough guide

Hook up sensor to rpi

SSH into the pi and install docker
```

curl -sSL https://get.docker.com/ | sh
sudo usermod -aG docker $USER
```
logout and in

Start project:
```
make start
```

Set up grafana sources, import dashboard etc. on 192.168.0.23:3000.

### Sources:
- https://github.com/adafruit/Adafruit_Python_DHT
- https://www.definit.co.uk/2018/07/monitoring-temperature-and-humidity-with-a-raspberry-pi-3-dht22-sensor-influxdb-and-grafana/




Find IP
```
$ ping raspberrypi.local
PING raspberrypi.local (192.168.1.138): 56 data bytes
```

Setup WIFI:
https://www.electronicshub.org/setup-wifi-raspberry-pi-2-using-usb-dongle/

#### Setup temp logger from Scratch

1. Use Raspberry Pi Imager to prepare the SD card
2. Add `ssh` file to the sd volume
3. Configure headless wifi https://www.raspberrypi.org/documentation/configuration/wireless/headless.md
4. Boot the pi and install Adafruit
```
git clone https://github.com/adafruit/Adafruit_Python_DHT.git && \
	cd Adafruit_Python_DHT && \
	python3 setup.py install && \
	cd ..
```
5. Clone the temperature api project 
```
git clone git@github.com:raspberry-commits/bedroom-temperature-api.git
```
6. Copy the ssh keys id_rsa and id_rsa.pub from last pass int ~/.ssh/
7. Install screen `sudo apt-get install screen`
8. Start the script in a screen
```
screen -d -m python3 rpi-temp-sensor/temp-logger-to-gh.py
```
Or add to /etc/rc.local
```
sudo vi /etc/rc.local
# Add to script
sudo su - pi -c "screen -dm -S tempsensor python3 /home/pi/rpi-temp-sensor/temp-logger-to-gh.py"
```