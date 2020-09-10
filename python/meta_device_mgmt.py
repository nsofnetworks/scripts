"""
This script creates a customized device settings and user settings.
In order to use this script, you must pass the following environment vars (API KEY and API ID that generated from the UI):
1. API_KEY_ID: <value>
2. API_KEY_SECRET: <value>
3. 'group_id': Replace with your group identifier that can be found in the UI.
4. 'idp_id': Replace with your IdP identifier that can be found in the UI
5. 'Allowed_Factors': Replace with one of the supported values: "SMS", "SOFTWARE_TOTP", "VOICECALL", "EMAIL"
6. Allowed factors can only be set for Non-SSO accounts
"""

import requests
import os
import pprint

# These are environment variables at the OS level
API_ENDPOINT = os.getenv("API_ENDPOINT", "https://api.metanetworks.com")
API_KEY_ID = os.environ["API_KEY_ID"]
API_KEY_SECRET = os.environ["API_KEY_SECRET"]

# Obtain access token and pass the necessary API credentials
def get_access_token():
    url = "%s/v1/oauth/token" % API_ENDPOINT
    request_data = {"grant_type": "client_credentials",
                    "client_id": API_KEY_ID,
                    "client_secret": API_KEY_SECRET}
    response = requests.post(url=url, json=request_data)
    response.raise_for_status()
    return response.json()['access_token']


# This function defines which device settings to configure
def create_device_settings(access_token, name, description, apply_to_entities, direct_sso, vpn_login_browser, split_tunnel,
                           session_lifetime, session_lifetime_grace, search_domains):
    url = "%s/v1/settings/device" % API_ENDPOINT
    headers = {'Authorization': 'Bearer %s' % access_token}
    body = {'name': name,
            'description': description,
            'apply_to_entities': apply_to_entities,
            'direct_sso': direct_sso,
            'vpn_login_browser': vpn_login_browser,
            'split_tunnel': True,
            'session_lifetime': session_lifetime,
            'session_lifetime_grace': session_lifetime_grace,
            'search_domains': search_domains}
    response = requests.post(url=url, json=body, headers=headers)
    response.raise_for_status()
    return response.json()


# This function defines which users settings to configure #
def create_user_settings(access_token, name, description, apply_to_entities, mfa_required, overlay_mfa_required,
                         overlay_mfa_refresh_period, allowed_factors, sso_mandatory):
    url = "%s/v1/settings/auth" % API_ENDPOINT
    headers = {'Authorization': 'Bearer %s' % access_token}
    body = {'name': name,
            'description': description,
            'apply_to_entities': apply_to_entities,
            'mfa_required': True,
            'overlay_mfa_required': True,
            'overlay_mfa_refresh_period': overlay_mfa_refresh_period,
            'allowed_factors': allowed_factors,
            'sso_mandatory': True}
    response = requests.post(url=url, json=body, headers=headers)
    response.raise_for_status()
    return response.json()


# This line uses the "PrettyPrinter" module to format the JSON data
if __name__ == '__main__':
    pp = pprint.PrettyPrinter(indent=4)
    token = get_access_token()
    print

# This line calls the "create_device_settings" function
    "Create device settings:"
    dev_settings = create_device_settings(token, "Device Settings Template", "Device Settings Template",
                                          ['group_id'], 'idp_id',
                                          "AGENT", True, 60, 30, ["example.com"])
    pp.pprint(dev_settings)
    print
    print

# This line calls the "create_user_settings" function (Only valid for Non-SSO accounts)
    "Create user settings:"
    user_settings = create_user_settings(token, "User Settings Template", "User Settings Template",
                                         ['group_id'], True, True, 10,
                                         ["Allowed_Factors"], True)
    pp.pprint(user_settings)
    print
    print
