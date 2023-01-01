import urllib3
import json
from datetime import datetime, timedelta
import os

urllib3.disable_warnings()
http = urllib3.PoolManager()


def lambda_handler(*args, **kwargs):
    monitor()


def get_last_recording():
    r = http.request("GET", "https://raw.githubusercontent.com/raspberry-commits/bedroom-temperature-api/master/temperature.json")
    data = json.loads(r.data.decode('utf-8'))

    return datetime.strptime(data['time'], '%Y-%m-%dT%H:%M:%SZ')


def monitor():
    last_recording = get_last_recording()
    one_hour_ago = datetime.now() - timedelta(hours=1)
    two_hours_ago = datetime.now() - timedelta(hours=2)
    if last_recording > one_hour_ago:
        print("All good")
        return

    print("Not good")
    if two_hours_ago > last_recording:
        print("Already alerted")
        return

    print("Sending notification")
    raise Exception("No recording from temperature sensor")


def is_running_in_lambda():
    return os.getenv("AWS_LAMBDA_FUNCTION_NAME", "") != ""


if is_running_in_lambda() is False:
    print("Running outside of Lambda")
    monitor()
