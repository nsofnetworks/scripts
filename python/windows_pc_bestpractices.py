"""
This script implements several Windows security posture checks best practices in audit (Log only mode).
In order to use this script, you must pass the following environment vars (API KEY and API ID that generated from the UI):
1. API_KEY_ID: <value>
2. API_KEY_SECRET: <value>
3. Acceptable action values are: "DISCONNECT" "NONE"
"""

import requests
import os
import pprint

# Defining the api-endpoint and API key here
API_ENDPOINT = os.getenv("API_ENDPOINT", "https://api.metanetworks.com")
API_KEY_ID = os.environ["API_KEY_ID"]
API_KEY_SECRET = os.environ["API_KEY_SECRET"]


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
def windows_best_practices(access_token, name, action, apply_to_org, interval, platform, when, osquery):
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

# Create list of Windows best practice security policies
# Customize as needed

# Check if Windows Update is enabled
    print
    "Create windows_update:"
    windows_update = windows_best_practices(token, "Windows Update Template", "NONE", True, 60, "Windows", ["PRE_CONNECT"],
                                      "SELECT * FROM services WHERE name='wuauserv' AND status LIKE 'RUNNING';")
    pp.pprint(windows_update)
    print
    print

# Check if Windows is domain joined
    print
    "Create windows_domain_joined:"
    windows_domain_joined = windows_best_practices(token, "Windows Domain Joined Template", "NONE", True, 60, "Windows", ["PRE_CONNECT"],
                                      "select data from registry where path='HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Group Policy\History\MachineDomain'"
                                      "and data='example.com';")
    pp.pprint(windows_domain_joined)
    print
    print

# Check if Windows BitLocker is enabled
    "Create windows_bitlocker:"
    windows_bitlocker_enabled = windows_best_practices(token, "Windows Bitlocker Template 1", "NONE", True, 60, "Windows",
                                        ["PRE_CONNECT"], "SELECT * FROM bitlocker_info WHERE protection_status = '1';")
    pp.pprint(windows_bitlocker_enabled)
    print

# Check if Windows BitLocker is enabled and only used disk is encrypted
    "Create windows_bitlocker:"
    windows_bitlocker_used_disk = windows_best_practices(token, "Windows Bitlocker Template 2", "NONE", True, 60, "Windows",
                                        ["PRE_CONNECT"],
                                        "SELECT * FROM bitlocker_info WHERE conversion_status AND protection_status = 1;")
    pp.pprint(windows_bitlocker_used_disk)
    print

# Check if Windows BitLocker is enabled and only used disk is encrypted and is using specific encryption method
    "Create windows_bitlocker:"
    windows_bitlocker_encryption_type = windows_best_practices(token, "Windows Bitlocker Template 2", "NONE", True, 60, "Windows",
                                        ["PRE_CONNECT"],
                                        "SELECT * FROM bitlocker_info WHERE conversion_status = ‘1’ AND protection_status = ‘1’ AND encryption_method LIKE ‘AES_128’;")
    pp.pprint(windows_bitlocker_encryption_type)
    print

# Check if Windows Defender is enabled
    "Create windows_defender Firewall:"
    windows_defender_firewall = windows_best_practices(token, "Windows Defender Firewall Template", "NONE", True, 60, "Windows", ["PRE_CONNECT"],
                                              "SELECT * FROM services WHERE name=‘MpsSvc’ OR ‘mpssvc’ AND status LIKE 'RUNNING';")
    pp.pprint(windows_defender_firewall)
    print
    print

# Check if Windows Defender AV is enabled
    "Create windows_defender AV:"
    windows_defender_av = windows_best_practices(token, "Windows Defender AV Template", "NONE", True, 60, "Windows", ["PRE_CONNECT"],
                                      "SELECT * FROM services WHERE name=‘WinDefend' AND status LIKE 'RUNNING';")
    pp.pprint(windows_defender_av)
    print
    print

# Check if Windows Defender ATP is enabled
    "Create windows_defender ATP:"
    windows_defender_atp = windows_best_practices(token, "Windows Defender ATP Template", "NONE", True, 60, "Windows", ["PRE_CONNECT"],
                                      "SELECT * FROM services WHERE name=‘Sense' AND status='RUNNING';")
    pp.pprint(windows_defender_atp)
    print
    print

# Check if Windows Defender AV NIS is enabled
    "Create Windows Defender AV NIS:"
    windows_defender_avnis = windows_best_practices(token, "Windows Defender AV NIS Template", "NONE", True, 60, "Windows", ["PRE_CONNECT"],
                                    "SELECT * FROM services WHERE name=‘WdNisSvc' AND status LIKE 'RUNNING';")
    pp.pprint(windows_defender_avnis)
    print
    print
