#! /usr/bin/python
from influxdb import InfluxDBClient
import os
import json

host = "localhost"
port = 8086
user = "rpi"
password = "rpi"
db_name = "sensor_data"
tempdata_path = "/home/pi/bedroom-temperature-api"
# tempdata_path = "/Users/jfinch/PersonalProjects/bedroom-temperature-api"
client = InfluxDBClient(host, port, user, password, db_name)
checkpoint_path = os.path.dirname(os.path.abspath(__file__)) + "/checkpoint.txt"


def reached_checkpoint(commit_hash):
    return commit_hash == get_checkpoint()


def save_checkpoint(commit_hash):
    if commit_hash is None:
        return
    f = open(checkpoint_path, "w")
    f.write(commit_hash)
    f.close()


def get_checkpoint():
    try:
        with open(checkpoint_path, "r") as f:
            return f.read().strip()
    except IOError:
        return False


def get_data(commit_hash):
    stream = os.popen("cd " + tempdata_path + " && git show " + commit_hash + ":temperature.json | cat")
    return [json.loads(stream.read())]


def write_data(data):
    if data[0]["fields"]["humidity"] is None or data[0]["fields"]["temperature"] is None:
        return
    client.write_points(data)


def pull_latest():
    os.popen("cd " + tempdata_path + " && git pull")


def get_commits_in_reverse_chronological():
    stream = os.popen("cd " + tempdata_path + " && git rev-list master")
    return stream.readlines()


def run():
    pull_latest()

    next_checkpoint = None
    for line in get_commits_in_reverse_chronological():
        commit_hash = line.strip()

        if next_checkpoint is None:
            next_checkpoint = commit_hash

        if reached_checkpoint(commit_hash) is True:
            break

        data = get_data(commit_hash)
        write_data(data)

    save_checkpoint(next_checkpoint)


run()
