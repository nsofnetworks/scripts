'''
version=1.0
this script will provide the ability to get devices data (agents & Meta Connect)

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

EORG=""
try:
    import json
except:
    print("please verify that the following packages installed: json\n if not you can install it by running  python -m pip install json")
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

#function to count the users in orgs
def userscount():
    url = "%s/v1/users" % API_ENDPOINT
    headers = {'Authorization': 'Bearer %s' % token}
    response = requests.get(url=url, headers=headers)
    r = response.json()
    ids = json_extract(r, 'id')
    maxusers = len(ids)
    return (maxusers)

#function to perform get request for recieving connected users data from meta api
def uniqueUsers():
    url = "%s/v1/metrics/unique/users/monthly?time_from=%sT00:00:00Z" % (API_ENDPOINT, inserted_time)
    headers = {'Authorization': 'Bearer %s' % token}
    response = requests.get(url=url, headers=headers)
    r = response.json()
    names = json_extract(r, 'value')
    return (names)
    #return str(names)[1:-1]

#function to add the number of missing zeros from date.
def create_laswithdate(last):
    lastnum=last
    # setting up the time plus one month
    date_time_obj = datetime.strptime(inserted_time, '%Y-%m-%d')
    end_date = datetime.now()
    num_months = (end_date.year - date_time_obj.year) * 12 + (end_date.month - date_time_obj.month)
    if len(lastnum) != num_months:
        gapmonths = num_months-len(lastnum)
        zero= [0] * gapmonths
        lastnum = zero + lastnum
    return(lastnum)
    #uncomment this for getting lasttime with date as a string
    '''
    x = 0
    tmpvar = ""
    for i in lastnum:
        date_time_obj = datetime.strptime(time, '%Y-%m-%d')
        one_mon_rel = relativedelta(months=x)
        date_time_obj = date_time_obj + one_mon_rel
        date_time_obj = date_time_obj.strftime('%B-%Y')
        print('Time:', date_time_obj + ":" + str(i) + " users")
        singlemonth = (date_time_obj + ":" + str(i) + " users")
        if x >= 1:
            lastwithdate = tmpvar + "," + singlemonth
        else:
            lastwithdate = singlemonth
        tmpvar = lastwithdate
        x += 1
    return(lastwithdate)
'''

#function to get months by names and not number
def getmonthnames():
    date_time_obj = datetime.strptime(inserted_time, '%Y-%m-%d')
    end_date = datetime.now()
    num_months = (end_date.year - date_time_obj.year) * 12 + (end_date.month - date_time_obj.month)
    x = 0
    coloumn = []
    for i in range(num_months):
        date_time_obj = datetime.strptime(inserted_time, '%Y-%m-%d')
        one_mon_rel = relativedelta(months=x)
        date_time_obj = date_time_obj + one_mon_rel
        date_time_obj = date_time_obj.strftime('%B-%Y')
        if x >= 1:
            coloumn = coloumn + " " + date_time_obj
        else:
            coloumn = date_time_obj
        tmpvar = coloumn
        x += 1
    return(coloumn.split(" "))


#getting time from system to create file name
now = datetime.now() # current date and time
current_time = now.strftime("%Y-%m-%d,%H-%M-%S")
filename = str("get_devices_data."+current_time)
sumnum = 0
agentsname=current_time+".agents_data."+EORG+".csv"
mcname=current_time+".mc_data."+EORG+".csv"

def Convert(lst):
    res_dct = {lst[i]: lst[i + 1] for i in range(0, len(lst), 2)}
    return res_dct

def AgentData():
    token = get_access_token()
    url = "%s/v1/network_elements?expand=true&connection=true" % API_ENDPOINT
    headers = {'Authorization': 'Bearer %s' % token}
    response = requests.get(url=url, headers=headers)
    data = response.json()
    token = get_access_token()
    url = "%s/v1/users" % API_ENDPOINT
    headers = {'Authorization': 'Bearer %s' % token}
    response = requests.get(url=url, headers=headers)
    r = response.json()
    f=open(agentsname, 'w',encoding="utf-8")
    title = "user ID,User Name,Family Name,Email,Device ID,Agent Version,Device Name,Platform version,Last Connection,\n"
    f.write(title)
    laststring=""
    for i in data:
        devicetype=json_extract(i, 'type')
        if devicetype == 'Device':
            deviceid= json_extract(i, 'id')
            agentversion=json_extract(i, 'agent_version')
            agentverison = json_extract(i, 'agent_version')
            devicename = json_extract(i, 'device_name')
            #platform = json_extract(i, 'platform')
            platform_version = json_extract(i,'platform_version')
            lastconnection=json_extract(i,'connected_at')
            userid=json_extract(i,'owner_id')
            for z in r:
                iduser=json_extract(z, 'id')
                if iduser==userid:
                    username = json_extract(z, 'given_name')
                    familyname= json_extract(z,'family_name')
                    email=json_extract(z,'email')
                    userdetails="%s,%s,%s" %(username,familyname,email)

            laststring="%s,%s,%s,%s,%s,%s,%s\n" %(userid,userdetails,deviceid,agentversion,devicename,platform_version,lastconnection)
            f.write(laststring)
        else:
            continue
    f.close()
    return (laststring)
def MetaConnectData():
    token = get_access_token()
    url = "%s/v1/metaconnects?connection=true" % API_ENDPOINT
    headers = {'Authorization': 'Bearer %s' % token}
    response = requests.get(url=url, headers=headers)
    data = response.json()
    token = get_access_token()
    url = "%s/v1/users" % API_ENDPOINT
    headers = {'Authorization': 'Bearer %s' % token}
    response = requests.get(url=url, headers=headers)
    r = response.json()
    f=open(mcname, 'w',encoding="utf-8")
    title = "last connection,user ID,device name,first name,last name,user email\n"
    f.write(title)
    laststring=""
    for i in data:
        deviceid = json_extract(i, 'id')
        lastconnection = json_extract(i, 'connected_at')
        userid = json_extract(i, 'owner_id')
        name = json_extract(i, 'name')
        for z in r:
            iduser = json_extract(z, 'id')
            if iduser == userid:
                username = json_extract(z, 'given_name')
                familyname = json_extract(z, 'family_name')
                email = json_extract(z, 'email')
                userdetails = "%s,%s,%s" % (username, familyname, email)

        laststring = "%s,%s,%s,%s\n" % (lastconnection, userid, name, userdetails)
        f.write(laststring)
    f.close()
    return (laststring)

def userselectmenu():
    userselect ='0'
    while userselect =='0':
        choice = input ("\nPlease select which data would you like to export:\n1.Agent Data\n2.Meta Conncet Data\n3.exit ")
        if choice == "1":
            print("starting to export agent data")
            Adata=AgentData()
            print("file has been save as " + agentsname)
        elif choice == "2":
            print("starting to export Meta Connect data")
            mcdata=MetaConnectData()
            print("file has been save as "+mcname)
        elif choice=="3":
            exit()
userselectmenu()