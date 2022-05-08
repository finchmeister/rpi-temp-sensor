# Raspberry Pi Home Temperature Monitoring System

- Raspberry Pi temperature sensor logger that pushes data to GitHub
- Raspberry Pi that fetches data from GitHub and imports it into Influxdb for visualisation with Grafana 

#### Setup Temp Logger from Scratch

1. Use [Raspberry Pi Imager](https://www.raspberrypi.org/software/) to prepare the SD card with Raspbian Lite
2. Add `ssh` file to the sd volume: `touch /Volumes/boot/ssh`
3. Configure headless wifi https://www.raspberrypi.org/documentation/configuration/wireless/headless.md. Add `wpa_supplicant.conf` to root directory.
```
vi /Volumes/boot/wpa_supplicant.conf
```
```
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country=GB

network={
 ssid="<WIFI NAME>"
 psk="<PASSWORD>"
}
```
4. Copy ssh keys with `ssh-copy-id pi@192.168.1.147`, password `raspberry`. Or just copy your local `id_rsa.pub` into `.ssh/authorized_keys` on the pi.
5. SSH into Pi and install dependencies
```
sudo apt-get update
sudo apt-get install git python3-pip -y
sudo python3 -m pip install --upgrade pip setuptools wheel
sudo pip3 install Adafruit_DHT
```
6. Clone the temperature sensor project 
```
git clone https://github.com/finchmeister/rpi-temp-sensor.git
```
7. Copy the ssh keys id_rsa and id_rsa.pub from last pass into ~/.ssh/ and set permission of id_rsa to 600 `sudo chmod 600 ~/.ssh/id_rsa`
8. Configure git
```
git config --global user.email "<EMAIL>"
git config --global user.name "Raspberry Commits"
```
9. Clone the temperature api project via ssh
```
git clone git@github.com:raspberry-commits/bedroom-temperature-api.git
```
10. Test the script. It should take a recording then push the data up to GitHub
```
python3 rpi-temp-sensor/temp-logger-to-gh.py
```
11. Run the script as a cron every 2 minutes

```
crontab -e

*/2 * * * * /usr/bin/python3 /home/pi/rpi-temp-sensor/temp-logger-to-gh.py >/dev/null 2>&1
```

#### Setup InfluxDb and Grafana

1. SSH into the pi and install docker
```

curl -sSL https://get.docker.com/ | sh
sudo usermod -aG docker $USER
```

2. Start Influxdb and Grafana:

```
make start-db
```

3. Set up grafana sources, import dashboard etc. on 192.168.1.148:3000.

4. Run the restore db command 

5. Setup the restore db to run as a cron task every minute
```
crontab -e

* * * * * /usr/bin/python3 /home/pi/rpi-temp-sensor/recover-git-data/restore_db.py >/dev/null 2>&1
```


### Sources:
- https://www.definit.co.uk/2018/07/monitoring-temperature-and-humidity-with-a-raspberry-pi-3-dht22-sensor-influxdb-and-grafana/
