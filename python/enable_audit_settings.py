"""
This script enables audit settings mode to log Internet traffic and enable Meta Connect logs for created users.
In order to use this script, you must pass the following environment vars (API KEY and API ID that generated from the UI):
1. API_KEY_ID: <value>
2. API_KEY_SECRET: <value>
3. Value "True" enable the option and "False" disables
"""

import requests
import os
import pprint

API_ENDPOINT = os.getenv("API_ENDPOINT", "https://api.metanetworks.com")
API_KEY_ID = os.environ["API_KEY_ID"]
API_KEY_SECRET = os.environ["API_KEY_SECRET"]


def get_access_token():
    url = "%s/v1/oauth/token" % API_ENDPOINT
    request_data = {"grant_type": "client_credentials",
                    "client_id": API_KEY_ID,
                    "client_secret": API_KEY_SECRET}
    response = requests.post(url=url, json=request_data)
    response.raise_for_status()
    return response.json()['access_token']


# Function to enable Internet Traffic
def enable_internet_traffic(access_token, log_internet_traffic):
    url = "%s/v1/settings/audit" % API_ENDPOINT
    headers = {'Authorization': 'Bearer %s' % access_token}
    body = {'log_internet_traffic': log_internet_traffic}
    response = requests.patch(url=url, json=body, headers=headers)
    response.raise_for_status()
    return response.json()


# Function to enable Internet Traffic
def enable_meta_connect(access_token, metaconnect_by_default=True):
    url = "%s/v1/settings/metaconnect" % API_ENDPOINT
    headers = {'Authorization': 'Bearer %s' % access_token}
    body = {'metaconnect_by_default': metaconnect_by_default}
    response = requests.patch(url=url, json=body, headers=headers)
    response.raise_for_status()
    return response.json()


if __name__ == '__main__':
    pp = pprint.PrettyPrinter(indent=4)
    token = get_access_token()


# This line calls the "enable_audit_settings" function
    print
    "Enable Internet Traffic:"
    internet_traffic = enable_internet_traffic(token, True)
    pp.pprint(internet_traffic)
    print


# This line calls the "enable_meta_connect" function
    print
    "Enable Meta Connect:"
    meta_connect_log = enable_meta_connect(token, True)
    pp.pprint(meta_connect_log)
    print
