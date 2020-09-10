"""
This script creates Egress PoP Exception rules for several Microsoft Services.
In order to use this script, you must pass the following environment vars:
1. API_KEY_ID: Your API Key ID
2. API_KEY_SECRET: Your API Key secret
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


# This function defines the Egress rule parameters #
def create_egress_rule(access_token, name, description, sources, destinations, via, enabled):
    url = "%s/v1/egress_routes" % API_ENDPOINT
    headers = {'Authorization': 'Bearer %s' % access_token}
    body = {'name': name,
            'description': description,
            'sources': sources,
            'destinations': destinations,
            'via': via,
            'enabled': True}
    response = requests.post(url=url, json=body, headers=headers)
    response.raise_for_status()
    return response.json()


if __name__ == '__main__':
    pp = pprint.PrettyPrinter(indent=4)
    token = get_access_token()
    print

# This line calls the "create_egress_rule function #
# Notice that the "exempt_sources" parameter is not yet available in the UI #
# The destination can also be a network object such as i.e "ne-500" #
    "Create egress Exchange Online:"
    egress_exchange_online = create_egress_rule(token, "MS-Exchange-Online", "Optimize Required", ['group_id'],
                                                ['outlook.office.com', 'outlook.office365.com', 'outlook.com', 'outlook.office.com',
                                                'smtp.office365.com', 'r1.res.office365.com', 'r3.res.office365.com', 'r4.res.office365.com',
                                                'attachments.office.net', 'protection.outlook.com', 'mail.protection.outlook.com',
                                                'measure.office.com'], "DIRECT", True)
    pp.pprint(egress_exchange_online)

    # Send Sharepoint and One-Drive via Ingress PoPAI #
    print
    "Create egress Sharepoint and OneDrive for Business:"
    egress_sharepoint_onedrive = create_egress_rule(token, "MS-Sharepoint-OneDrive", "Optimize Required", ['group_id'],
                                                    ['sharepoint.com', 'log.optimizely.com', 'search.production.apac.trafficmanager.net',
                                                     'search.production.emea.trafficmanager.net', 'search.production.us.trafficmanager.ne',
                                                     'wns.windows.com', 'admin.onedrive.com', 'officeclient.microsoft.com',
                                                     'g.live.com', 'oneclient.sfx.ms', 'sharepointonline.com',
                                                     'cdn.sharepointonline.com', 'privatecdn.sharepointonline.com', 'publiccdn.sharepointonline.com',
                                                     'spoprod-a.akamaihd.net', 'static.sharepointonline.com', 'prod.msocdn.com', 'watson.telemetry.microsoft.com',
                                                     'svc.ms'], "DIRECT", True)
    pp.pprint(egress_sharepoint_onedrive)

    # Send MS-Skype and Teams Direct via Ingress PoPAI #
    print
    "Create egress Skype for Business and Teams:"
    egress_skype_teams = create_egress_rule(token, "MS-Skype-Teams", "Optimize Required", ['group_id'],
                                                    ['lync.com', 'teams.microsoft.com', 'broadcast.skype.com', 'quicktips.skypeforbusiness.com',
                                                     'sfbassets.com', 'urlp.sfbassets.com', 'skypemaprdsitus.trafficmanager.net',
                                                     'keydelivery.mediaservices.windows.net', 'msecnd.net', 'streaming.mediaservices.windows.net',
                                                     'ajax.aspnetcdn.co', 'mlccdn.blob.core.windows.net', 'aka.ms', 'amp.azure.net',
                                                     'users.storage.live.com', 'adl.windows.com', 'skypeforbusiness.com',
                                                     'msedge.net', 'compass-ssl.microsoft.com', 'mstea.ms', 'secure.skypeassets.com',
                                                     'mlccdnprod.azureedge.net', 'assets.com', 'mlccdnprod.azureedge.net',
                                                     'videoplayercdn.osi.office.net', 'tenor.com', 'skype.com', 'statics.teams.microsoft.com'], "DIRECT", True)
    pp.pprint(egress_skype_teams)
    print
