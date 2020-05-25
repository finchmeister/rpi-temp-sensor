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

