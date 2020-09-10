"""
This script implements several macOS security posture checks best practices in audit (Log only mode).
In order to use this script, you must pass the following environment vars (API KEY and API ID that generated from the UI):
1. API_KEY_ID: <value>
2. API_KEY_SECRET: <value>
3. Acceptable action values are: "DISCONNECT" "NONE"
"""

import requests
import os
import pprint

# Defining the api-endpoint and API key here
API_ENDPOINT = os.getenv("NSOF_API_ENDPOINT", "https://api.metanetworks.com")
API_KEY_ID = os.environ["NSOF_API_KEY_ID"]
API_KEY_SECRET = os.environ["NSOF_API_KEY_SECRET"]


# Getting API Access token
def get_access_token():
    url = "%s/v1/oauth/token" % API_ENDPOINT
    request_data = {"grant_type": "client_credentials",
                    "client_id": API_KEY_ID,
                    "client_secret": API_KEY_SECRET}
    response = requests.post(url=url, json=request_data)
    response.raise_for_status()
    return response.json()['access_token']


# Function to enable common posture check options in Audit Mode
# Customize as needed
def macos_best_practices(access_token, name, action, apply_to_org, interval, platform, when, osquery):
    url = "%s/v1/posture_checks" % API_ENDPOINT
    headers = {'Authorization': 'Bearer %s' % access_token}
    body = {'name': name,
            'action': action,
            'apply_to_org': True,
            'interval': interval,
            'platform': platform,
            'when': when,
            'osquery': osquery}
    response = requests.post(url=url, json=body, headers=headers)
    response.raise_for_status()
    return(response.json())


if __name__ == '__main__':
    pp = pprint.PrettyPrinter(indent=4)
    token = get_access_token()

# Create list of MacOS best practice security policies
# Customize as needed
    print
    "Create macos_domain_joined:"
    macos_domain_joined = macos_best_practices(token, "MacOS Domain Joined Template", "NONE", True, 60, "macOS", ["PRE_CONNECT"],
                                      "SELECT * FROM ad_config WHERE value = 'example.com';")
    pp.pprint(macos_domain_joined)
    print
    print
    "Create macos_remote_login:"
    remote_login = macos_best_practices(token, "MacOS Remote Login Template", "NONE", True, 60, "macOS", ["PRE_CONNECT"],
                                      "SELECT * FROM sharing_preferences WHERE remote_login = '0';")
    pp.pprint(remote_login)
    print
    print
    "Create macos_enable_gatekeeper:"
    macos_gatekeeper = macos_best_practices(token, "MacOS Gatekeeper Template", "NONE", True, 60, "macOS", ["PRE_CONNECT"],
                                      "SELECT * FROM gatekeeper where assessment_enabled = '1';")
    pp.pprint(macos_gatekeeper)
    print
    print
    "Create macos_stealth_mode:"
    macos_stealth_mode= macos_best_practices(token, "MacOS Stealth Mode Template", "NONE", True, 60, "macOS", ["PRE_CONNECT"],
                                      "SELECT * FROM alf WHERE stealth_enabled = '1';")
    pp.pprint(macos_stealth_mode)
    print
    print
    "Create macos_application_firewall:"
    macos_app_firewall = macos_best_practices(token, "MacOS App Firewall Template", "NONE", True, 60, "macOS", ["PRE_CONNECT"],
                                      "SELECT * FROM alf WHERE global_state = '1';")
    pp.pprint(macos_app_firewall)
    print
    print
    "Create macos_sip:"
    macos_sip = macos_best_practices(token, "MacOS SIP Configuration Template", "NONE", True, 60, "macOS", ["PRE_CONNECT"],
                                    "SELECT * FROM sip_config WHERE config_flag = 'sip' AND enabled = '1';")
    pp.pprint(macos_sip)
    print
    print
    "Create macos_screensharing:"
    macos_screen_sharing = macos_best_practices(token, "MacOS Screen Sharing Template", "NONE", True, 60, "macOS", ["PRE_CONNECT"],
                                              "SELECT * FROM sharing_preferences WHERE screen_sharing = '0';")
    pp.pprint(macos_screen_sharing)
    print
    print
    "Create macos_autoupdate:"
    macos_autoupdate = macos_best_practices(token, "MacOS AutoUpdate Template", "NONE", True, 60, "macOS", ["PRE_CONNECT"],
                                      "SELECT * FROM preferences WHERE key = 'AutoUpdate' AND value = 'true';")
    pp.pprint(macos_autoupdate)
    print
    print
    "Create macos_filevault Option 1:"
    macos_filevault_option1 = macos_best_practices(token, "MacOS FileVault Template (Option 1)", "NONE", True, 60, "macOS", ["PRE_CONNECT"],
                                        "SELECT d.encrypted FROM mounts m JOIN disk_encryption D on m.device_alias = d.name WHERE m.path = '/';")
    pp.pprint(macos_filevault_option1)
    print
    print
#    "Create macos_filevault Option 2:"
#    macos_filevault_option2 = macos_best_practices(token, "MacOS FileVault Template (Option 2)", "NONE", False, 60, "macOS", ["PRE_CONNECT"],
#                                      "SELECT m.path, m.type as mount_type, round((m.blocks_available * m.blocks_size * 10e-10) ,2) as free_gigs, de.encrypted, de.type from mounts m join disk_encryption de on de.name=m.device where m.path ='/' and de.encrypted='1';")
#    pp.pprint(macos_filevault_option2)
#    print
#    print
