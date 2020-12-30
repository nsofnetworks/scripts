'''
version=1.0
this script will provide the ability to get active unique users per day (for MSSP - please fill the EORG-value)
reading the API keys has 2 options (file or env variables),by default the script will try to read from file and if not defined it will
proceed to read from environemnt varaibles:

reading from file:
Please fill the path to API_KEY_ID_PATH,API_KEY_SECRET_PATH,ORGS_LIST_PATH before running the script (only csv or txt file)
Example: "C:\\Users\\administrator\\Desktop\\ID.csv"

reading from env variables:
the varaibles should be added as the following:
API_KEY_ID = value
API_KEY_SECRET = value
'''
import os
import sys


API_KEY_ID_PATH = "Replace this text with the path to the API ID file"
API_KEY_SECRET_PATH = "Replace this text with the path to the API secret file"
ORGS_LIST_PATH = "replace this string with the path to the file with the org shortname that you like to run this script"

EORG="ironsource"
try:
    import json
except:
    print("please verify that the following packages installed: json\n if not you can install it by running  python -m pip install json")
    exit()
try:
    import datetime
except:
   print("please verify that the following packages installed: datetime\n if not you can install it by running  python -m pip install datetime")
   exit()
try:
    import extract
except:
    print("please verify that the following packages installed: extract\n if not you can install it by running  python -m pip install extract")
    exit()
try:
    import requests
except:
    print("please verify that the following packages installed: requests\n if not you can install it by running  python -m pip install requests")
    exit()


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
            print("reading the API keys has 2 options (file or env variables),by default the script will try to read from file and if not defined it will\n"
                  "proceed to read from environemnt varaibles:\n"
                  "reading from file:\n"
                  "Please fill the path to API_KEY_ID_PATH,API_KEY_SECRET_PATH,ORGS_LIST_PATH before running the script (only csv or txt file)\n"
                  "Example: 'C:\\Users\\administrator\\Desktop\\ID.csv'\n"
                  "reading from env variables:"
                  "the varaibles should be added as the following:\n"
                  "API_KEY_ID = value\n"
                  "API_KEY_SECRET = value\n")
            exit()
except:
    print(
        "please verify the path to API_KEY_ID and API_KEY_SECRET or your env variables and also that the key is valid with write privilege"
        "to users")
    exit()

#Function to extract nested Json
def json_extract(obj, key):
    """Recursively fetch values from nested JSON."""
    arr = []

    def extract(obj, arr, key):
        """Recursively search for values of key in JSON tree."""
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, (dict, list)):
                    extract(v, arr, key)
                elif k == key:
                    arr.append(v)
        elif isinstance(obj, list):
            for item in obj:
                extract(item, arr, key)
        return arr
    values = extract(obj, arr, key)
    values= str(values).replace('[',"")
    values = str(values).replace(']', "")
    values = str(values).replace('\'', "")
    return (values)

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
                            "scope": "org:%s" % EORG}
        response = requests.post(url=url, json=request_data)
        response.raise_for_status()
        return response.json()['access_token']
    except Exception as e:
        print("please verify the path to API_KEY_ID and API_KEY_SECRET and also that the key is valid with write "
              "privilege to users")
        print(e)
        exit()


def active_users_per_day():
    select_number_of_days= int(input("please enter the number of days to recieve the report:\n"))
    # getting time from system to create file name
    x = datetime.datetime.now() - datetime.timedelta(select_number_of_days)
    minus30daysY = x.strftime("%Y-%m-%d")
    minus30daysM = x.strftime("%H:%M:%S")
    string=minus30daysY+"T"+minus30daysM+"Z"
    token = get_access_token()
    url = '%s/v1/metrics/unique/users/daily?time_from=%s' %(API_ENDPOINT,string)
    headers = {'Authorization': 'Bearer %s' % token}
    response = requests.get(url=url, headers=headers)
    data = response.json()
    day = json_extract(data, 'key')
    number= json_extract(data, 'value')
    z=number.split(",")
    y=day.split(",")
    x = x - datetime.timedelta(1)
    for i,o in zip(y,z):
        tempname = (datetime.datetime.fromtimestamp(int(i) / 1000).strftime("%Y,%B %d"))
        print(tempname+":",o)
active_users_per_day()
