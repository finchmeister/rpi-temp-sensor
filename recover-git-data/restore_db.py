#! /usr/bin/python
from influxdb import InfluxDBClient
import os
import json

host = "localhost"
port = 8086
user = "rpi"
password = "rpi"
db_name = "sensor_data"
tempdata_path = "/Users/jofinch/PersonalProjects/bedroom-temperature-api"
client = InfluxDBClient(host, port, user, password, db_name)


def get_data(commit_hash):
    stream = os.popen("cd " + tempdata_path + " && git show " + commit_hash + ":temperature.json | cat")
    data = [json.loads(stream.read())]
    print(data)
    write_data(data)


def write_data(data):
    if data[0]["fields"]["humidity"] is None or data[0]["fields"]["temperature"] is None:
        return
    client.write_points(data)

# Loop through every commit

# stream = os.popen("cd " + tempdata_path + " && git rev-list --reverse master")
stream = os.popen("cd " + tempdata_path + " && git rev-list master")
output = stream.readlines()

i = 0

for line in output:
    commit_hash = line.strip()
    print(i)
    i = i+1
    print(get_data(commit_hash))
