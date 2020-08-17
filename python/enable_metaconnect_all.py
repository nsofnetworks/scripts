import os
import sys
import subprocess
import pprint
import csv
import json
import argparse
import pkg_resources


'''This script will provide the option to enable to option for all org users to meta connect 

reading the API keys has 2 options (file,env variables),by default the script will try to read from file and if not defined it will
proceed to read from environemnt varaibles:

reading from file:
Please fill the path to API_KEY_ID_PATH and API_KEY_SECRET_PATH before running the script (only csv or txt file)
Example: "C:\\Users\\administrator\\Desktop\\ID.csv"

reading from env variables:
the varaibles should be added as the following:
API_KEY_ID = value
API_KEY_SECRET = value
EORG = value
'''

API_KEY_ID_PATH = "Replace this text with the path to the API ID file"
API_KEY_SECRET_PATH = "Replace this text with the path to the API secret file"
EORG_PATH = "replace this string with the path to the file with the org shortname that you like to run this script"

# -h or --help text
parser = argparse.ArgumentParser(
    description="this script will provide the option to create multiple users that has been writen in a csv file,\n"
                "the csv file format should be as following: email,description,family name,first name,phone (optional)")
args = parser.parse_args()

# checking if requests package installed and installing it if not.
required = {'requests'}
installed = {pkg.key for pkg in pkg_resources.working_set}
missing = required - installed
if missing:
    python = sys.executable
    subprocess.check_call([python, '-m', 'pip', 'install', *missing], stdout=subprocess.DEVNULL)
import requests

# read the ID and Secret from file or from env variables
API_ENDPOINT = os.getenv("NSOF_API_ENDPOINT", "https://api.metanetworks.com")
try:
    try:
        with open(API_KEY_ID_PATH, "r") as file:
            API_KEY_ID = file.readline().replace('\n', '')
        with open(API_KEY_SECRET_PATH, "r") as file:
            API_KEY_SECRET = file.readline().replace('\n', '')
    except:
        print("Keys didn't found in the supplied path\nchecking for keys in the environment variables")
        try:
            API_KEY_ID = os.environ['API_KEY_ID']
            API_KEY_SECRET = os.environ['API_KEY_SECRET']
        except:
            print("Keys also didn't found in the os variables")
    try:
        with open(EORG_PATH, "r") as file:
            EORG = file.readline().replace('\n', '')
    except:
        print("sub org didn't found\nchecking for EORG in the environment variables")
        try:
            EORG = os.environ['EORG']
        except:
            print("sub org didn't defined in the environment varaibles")
            EORG = None
            pass
except:
    print(
        "please verify the path to API_KEY_ID and API_KEY_SECRET or your env variables and also that the key is valid with write privilege"
        "to users")
    exit()

EORGorig = "replace this string with the path to the file with the org shortname that you like to run this script"
# function to get access token
def get_access_token():
    url = "%s/v1/oauth/token" % API_ENDPOINT
    try:
        if EORG is None:
            request_data = {"grant_type": "client_credentials",
                            "client_id": API_KEY_ID,
                            "client_secret": API_KEY_SECRET}
        else:
            request_data = {"grant_type": "client_credentials",
                            "client_id": API_KEY_ID,
                            "client_secret": API_KEY_SECRET,
                            "scope: org":EORG}
        response = requests.post(url=url, json=request_data)
        response.raise_for_status()
        return response.json()['access_token']
    except Exception as e:
        print("please verify the path to API_KEY_ID and API_KEY_SECRET and also that the key is valid with write "
              "privilege to users")
        print(e)
        exit()
token = get_access_token()

url = "%s/v1/users" % API_ENDPOINT
headers = {'Authorization': 'Bearer %s' % token}

response = requests.get(url=url, headers=headers)
users = json.loads(response.content)
url = "%s/v1/metaconnects" % API_ENDPOINT
for user in users:
    if any(p.startswith('mc-') for p in user['inventory']):
        print("[%s] already exists" % user['id'])
        continue
    name = "%s's MetaConnect" % user['name']
    body = {"owner_id": user['id'], "name": name}
    response = requests.post(url=url, json=body, headers=headers)
    mc = json.loads(response.content)
    print("[%s] created %s" % (user['id'], mc['id']))