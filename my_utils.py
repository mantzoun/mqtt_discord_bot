import requests
import json
import os

def my_hostname():
    return os.uname()[1]

def my_public_ip():
    res = requests.get('https://ipinfo.io/json', verify = True)

    if res.status_code != 200:
        return res.status_code, "Error getting public IP"

    return res.status_code, res.json()['ip']
