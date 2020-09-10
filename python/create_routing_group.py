"""
This script creates a single user routing group containing the group "All Users" as source.
In order to use this script, you must pass the following environment vars (API KEY and API ID that generated from the UI):
1. API_KEY_ID: <value>
2. API_KEY_SECRET: <value>
3. 'group_id': Replace with your group identifier that can be found in the UI.
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


def create_routing_group(access_token, name, description, exempt_sources, sources, mapped_elements_ids):
    url = "%s/v1/routing_groups" % API_ENDPOINT
    headers = {'Authorization': 'Bearer %s' % access_token}
    body = {'name': name,
            'description': description,
            'exempt_sources': exempt_sources,
            'sources': sources,
            'mapped_elements_ids': mapped_elements_ids}
    response = requests.post(url=url, json=body, headers=headers)
    response.raise_for_status()
    return response.json()

if __name__ == '__main__':
    pp = pprint.PrettyPrinter(indent=4)
    token = get_access_token()
    print
    "Create routing group:"
    routing_group = create_routing_group(token, "Meta URG Template", "Meta URG Template",
                                         ['group_id'])
    pp.pprint(routing_group)
    print
    print
