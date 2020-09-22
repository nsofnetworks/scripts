import os
import sys
import json
try:
    import requests
except:
    print("please verify that the following packages installed: requests\n if not please run python -m pip install <pkgName>")
    exit()

'''this script will provide the ability to create "content categories" with a list of URL's or cntents categories

reading the API keys has 2 options (file,env variables),by default the script will try to read from file and if not defined it will
proceed to read from environemnt varaibles:

reading from file:
Please fill the path to API_KEY_ID_PATH,API_KEY_SECRET_PATH,ORGS_LIST_PATH before running the script (only csv or txt file)
Example: "C:\\Users\\administrator\\Desktop\\ID.csv"

reading from env variables:
the varaibles should be added as the following:
API_KEY_ID = value
API_KEY_SECRET = value
'''

#optional if didn't added to the os env variable
API_KEY_ID_PATH = "Replace this text with the path to the API ID file"
API_KEY_SECRET_PATH = "Replace this text with the path to the API secret file"
#please enter the path to the URL list file
'''file content structure should be as following(please verify you have no spaces at end of line):
domainA.com
domainB.com
'''
URLS_LIST_PATH = "replace this string with the path to the file with the URL's that you like to create"
#optional
CONTENT_CATEGORIES_PATH = "replace this string with the path to the file with content categories that you like to create, be aware that the content category is case sensitive"

#optional for MSSP'S or multi tenants customers
EORG = None

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
        with open(URLS_LIST_PATH, "r") as file:
            urlslist = file.read().split("\n")
            print(urlslist)
    except:
        print("URLS_LIST_PATH path didn't defined or can't read from file")
        exit()
    try:
        with open(CONTENT_CATEGORIES_PATH, "r") as file:
            contentlist = file.read().split("\n")
            print(contentlist)
    except:
        print("CONTENT_CATEGORIES_PATH didn't defined or can't read from file")
        contentlist = None

except:
    print(
        "please verify the path to API_KEY_ID and API_KEY_SECRET or your env variables and also that the key is valid with write privilege"
        "to users")
    exit()

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

token = get_access_token()
url = "%s/v1/content_categories" % API_ENDPOINT
headers = {'Authorization': 'Bearer %s' % token}
name = input("please enter name for the content categories:")
description = input("please enter description for the content categories:")
if contentlist is None:
    body = {'name': name, 'urls': urlslist, 'description': description}
else:
    body = {'name': name, 'urls': urlslist, 'types': contentlist, 'description': description}
response = requests.post(url=url,json=body, headers=headers)
r = response.json()
print(r)
exit()
