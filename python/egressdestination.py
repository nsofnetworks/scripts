import os
import sys
import json

'''this script will provide the ability to patch multiple destinations to existing egress rule from file

reading the API keys has 2 options (file,env variables),by default the script will try to read from file and if not defined it will
proceed to read from environemnt varaibles:

reading from file:
Please fill the path to API_KEY_ID_PATH,API_KEY_SECRET_PATH,EORG(optional for MSSP's),FILE_CONTENT_PATH,EGRESS_ID_PATH before running the script (only csv or txt file)
Example: "C:\\Users\\administrator\\Desktop\\ID.csv"

reading from env variables:
the varaibles should be added as the following:
API_KEY_ID = value
API_KEY_SECRET = value
EORG = value
EGRESS_ID = value
'''

API_KEY_ID_PATH = "Replace this text with the path to the API ID file"
API_KEY_SECRET_PATH = "Replace this text with the path to the API secret file"
EORG_PATH = "replace this string with the path to the file with the org shortname that you like to run this script"
EGRESS_ID_PATH = "replace this string with the path to the file with the Egress ID that you like to run this script on"
'''file content structure should be as following(please verify you have no spaces at end of line):
domainA.com
domainB.com
doaminC.com
'''
FILE_CONTENT_PATH="replace this string with the path to the file content"


# -h or --help text
parser = argparse.ArgumentParser(
    description="this script will provide the option to create multiple destination to egress rule,\n"
                'the providing list should be in the following structure - "google.com","amazon.com","foo.com"')
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
    try:
        with open(EGRESS_ID_PATH, "r") as file:
            EGRESS_ID = file.readline().replace('\n', '')
    except:
        print("EGRESS ID didn't found\nchecking for EGRESS ID in the environment variables")
        try:
            EGRESS_ID = os.environ['EGRESS_ID']
        except:
            print("EGRESS ID didn't defined in the environment varaibles\nplease verify that the path for EGRESS ID is correct or the value exist in the environment variables")
            exit()
    try:
        with open(FILE_CONTENT_PATH, "r") as file:
            filecontent = file.read().split("\n")
            print(filecontent)
    except:
        print("EGRESS ID didn't found\nchecking for EGRESS ID in the environment variables")

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

url = "%s/v1/egress_routes/%s" % (API_ENDPOINT, EGRESS_ID)
headers = {'Authorization': 'Bearer %s' % token}
body = {'destinations': filecontent}
response = requests.patch(url=url, json=body, headers=headers)
r = json.loads(response.content)
print(r)

