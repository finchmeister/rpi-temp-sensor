# Raspberry Pi Home Temperature Monitoring System


Requirements

- Raspberry Pi
- DHT22 temperature & humidity sensor

## Rough guide

Set up sensor

Install docker
```

curl -sSL https://get.docker.com/ | sh
sudo usermod -aG docker $USER
```
logout and in
```
sudo apt-get install docker-compose
sudo apt-get install python-pip
sudo pip install influxdb
```
Install the Python library to read from the sensor:
```
git clone https://github.com/adafruit/Adafruit_Python_DHT.git
cd Adafruit_Python_DHT
python setup.py install
```

Start project:
```
make start
```

Set up grafana etc. on 192.168.0.23:3000.

## Todo:
- [ ] Dockerise python script https://github.com/farshidtz/Adafruit_Python_DHT_Docker https://hub.docker.com/r/arm32v6/python/
- [ ] 

## Sources:
- https://github.com/adafruit/Adafruit_Python_DHT
- https://www.definit.co.uk/2018/07/monitoring-temperature-and-humidity-with-a-raspberry-pi-3-dht22-sensor-influxdb-and-grafana/