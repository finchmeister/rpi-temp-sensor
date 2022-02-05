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


def send_notification_via_pushbullet(title, body):
    """ Sending notification via pushbullet.
        Args:
            title (str) : title of text.
            body (str) : Body of text.
    """
    data_send = {"type": "note", "title": title, "body": body}

    access_token = os.getenv("PUSHBULLET_ACCESS_TOKEN", "")

    if access_token == "":
        raise Exception("PUSHBULLET_ACCESS_TOKEN env not set")

    resp = http.request(
        "POST",
        "https://api.pushbullet.com/v2/pushes",
        body=json.dumps(data_send),
        headers={'Authorization': 'Bearer ' + access_token, 'Content-Type': 'application/json'}
    )

    if resp.status != 200:
        response_data = {
            "status" : resp.status,
            "data" : resp.data,
            "headers": resp.headers
        }
        print(response_data)
        raise Exception('Something wrong sending notification: ')

    print('Notification sent')


def monitor():
    last_recording = get_last_recording()
    one_hour_ago = datetime.now() - timedelta(hours=1)
    three_hours_ago = datetime.now() - timedelta(hours=3)
    if last_recording > one_hour_ago:
        print("All good")
        return

    print("Not good")
    if three_hours_ago > last_recording:
        print("Already alerted")
        return

    print("Sending notification")
    send_notification_via_pushbullet("Temperature Sensor", "It is fucked mate")


def is_running_in_lambda():
    return os.getenv("AWS_LAMBDA_FUNCTION_NAME", "") != ""


if is_running_in_lambda() is False:
    print("Running outside of Lambda")
    monitor()
