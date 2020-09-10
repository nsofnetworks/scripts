"""
This script configure the version control feature profile.
In order to use this script, you must pass the following environment vars (API KEY and API ID that generated from the UI):
1. API_KEY_ID: <value>
2. API_KEY_SECRET: <value>
3. Replace "mode" with your desired value: "disable" "specific_version" "latest_stable" "latest_beta"
"""

import requests
import os
import pprint

# These are environment variables at the OS level #
API_ENDPOINT = os.getenv("API_ENDPOINT", "https://api.metanetworks.com")
API_KEY_ID = os.environ["API_KEY_ID"]
API_KEY_SECRET = os.environ["API_KEY_SECRET"]


# Obtain access token and pass the necessary API credentials #
def get_access_token():
    url = "%s/v1/oauth/token" % API_ENDPOINT
    request_data = {"grant_type": "client_credentials",
                    "client_id": API_KEY_ID,
                    "client_secret": API_KEY_SECRET}
    response = requests.post(url=url, json=request_data)
    response.raise_for_status()
    return response.json()['access_token']


# Function to enable version control options
def create_version_control(access_token, name, description, apply_to_org, windows_policy, macos_policy, linux_policy):
    url = "%s/v1/version_controls" % API_ENDPOINT
    headers = {'Authorization': 'Bearer %s' % access_token}
    body = {'name': name,
            'description': description,
            'apply_to_org': apply_to_org,
            'windows_policy': windows_policy,
            'macos_policy': macos_policy,
            'linux_policy': linux_policy}
    response = requests.post(url=url, json=body, headers=headers)
    response.raise_for_status()
    return response.json()


if __name__ == '__main__':
    pp = pprint.PrettyPrinter(indent=4)
    token = get_access_token()


# Call create_version_control function
    print
    "Create version control policy:"
    global_version_control = create_version_control(token, "Meta Version Control ", "Version Control Template", True,
                                                    windows_policy={"mode": "latest_stable"},
                                                    macos_policy={"mode": "latest_stable"},
                                                    linux_policy={"mode": "latest_stable"})
    pp.pprint(global_version_control)
    print
    print
