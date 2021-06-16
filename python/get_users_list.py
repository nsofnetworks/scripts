import os
import sys
import json
try:
    import requests
except:
    print("please verify that the following packages installed: requests\n if not please run python -m pip install <pkgName>")
    exit()
try:
    from datetime import date, timedelta,datetime
except:
    print("please verify that the following packages installed: datetime\n if not you can install it by running  python -m pip install datetime")
    exit()

try:
    import time
except:
    print("please verify that the following packages installed: time\n if not you can install it by running  python -m pip install time")
    exit()
'''this script will provide the ability to get users list in org to CSV file, the content of the CSV is as following: ID,Email,First name,Last name

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
EORG = ""


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

except:
    print('please verify the path to API_KEY_ID and API_KEY_SECRET or your env variables and also that the key is valid with write privilege to users\nreading the API keys has 2 options (file,env variables),by default the script will try to read from file and if not defined it will proceed to read from environemnt varaibles:\nreading from file:\nPlease fill the path to API_KEY_ID_PATH,API_KEY_SECRET_PATH,ORGS_LIST_PATH before running the script (only csv or txt file)\nExample: "C:\\Users\\administrator\\Desktop\\ID.csv"\nreading from env variables:\nthe varaibles should be added as the following:\nAPI_KEY_ID = value\nAPI_KEY_SECRET = value')
    exit()

# function to get access token
def get_access_token():
    url = "%s/v1/oauth/token" % API_ENDPOINT
    try:
        if EORG is None:
            request_data = {"grant_type": "client_credentials",
                            "client_id": API_KEY_ID,
                            "client_secret": API_KEY_SECRT}
        else:
            request_data = {"grant_type": "client_credentials",
                            "client_id": API_KEY_ID,
                            "client_secret": API_KEY_SECRET,
                            "scope": "org:%s" % EORG}
        response = requests.post(url=url, json=request_data)
        response.raise_for_status()
        return response.json()['access_token']
    except Exception as e:
        print('please verify the path to API_KEY_ID and API_KEY_SECRET and also that the key is valid with write\nprivilege to users\nreading the API keys has 2 options (file,env variables),by default the script will try to read from file and if not defined it will proceed to read from environemnt varaibles:\nreading from file:\nPlease fill the path to API_KEY_ID_PATH,API_KEY_SECRET_PATH,ORGS_LIST_PATH before running the script (only csv or txt file)\nExample: "C:\\Users\\administrator\\Desktop\\ID.csv"\nreading from env variables:\nthe varaibles should be added as the following:\nAPI_KEY_ID = value\nAPI_KEY_SECRET = value')
        print(e)
        exit()
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

#create a name and get time for file name
now = datetime.now() # current date and time
date=now.strftime("%Y-%m-%d,%H-%M-%S")
fname=EORG+".users.list."+date+".csv"
f = open(fname, 'w', encoding="utf-8")
title = "user ID,email,first name,last name,status\n"
f.write(title)

Next="a"
num=1
page_num = 1
B=1
while B==1:
    # getting access token and starting parameters for loop
    token = get_access_token()
    # count time for refresh token
    import time
    start_time = time.time()
    t_end = time.time() + 60 * 3
    #if to done a loop
    if Next == "":
        B = 10

    #while loop to get the users list and pharse data from each user to CSV file
    while Next!= "" and time.time() < t_end:
        if num==1:
            url = "%s/v1/users?pagination=true&page_size=1000" % API_ENDPOINT
            num=2
        else:
            url = "%s/v1/users?pagination=true&page=%s" % (API_ENDPOINT,Next)
        headers = {'Authorization': 'Bearer %s' % token}
        response = requests.get(url=url, headers=headers)
        r = response.json()
        print(r)
        print("page number "+str(page_num)+" downloaded (1000 users per page)")
        page_num=page_num+1

        #pagination for recieving 1000 users per request (1000 is the limit)
        try:
            Next=r['next']
        except:
            Next=""
            B = 10
        for i in r['items']:
            iduser = json_extract(i, 'id')
            email = json_extract(i, 'email')
            first_name = json_extract(i, 'given_name')
            last_name = json_extract(i, 'family_name')
            status = json_extract(i,'enabled')
            laststring = "%s,%s,%s,%s,%s\n" % (iduser, email, first_name, last_name,status)
            f.write(laststring)

print("script done successfully, file has been saved as:")
print(fname)
exit()
