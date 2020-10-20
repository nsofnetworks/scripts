'''
version=1.0
this script will provide the ability to get number of connected unique users per month. please verify that you fill the "inserted_date" parameter (line 21)
this script has 2 options - reading from org list or by typing the shortname of the tenant

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

#the convention of time is year-month-day, be awre that the day always should be 01.
inserted_time = "2020-01-01"

API_KEY_ID_PATH = "Replace this text with the path to the API ID file"
API_KEY_SECRET_PATH = "Replace this text with the path to the API secret file"
ORGS_LIST_PATH = "replace this string with the path to the file with the org shortname that you like to run this script"
'''file content structure should be as following(please verify you have no spaces at end of line):
shortnameA
shortnameB
shortnameC
'''

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
try:
    import csv
except:
    print("please verify that the following packages installed: csv\n if not you can install it by running  python -m pip install csv")
    exit()
try:
    from prettytable import PrettyTable
except:
    print("please verify that the following packages installed: prettytable\n if not you can install it by running  python -m pip install prettytable")
    exit()
try:
    from dateutil.relativedelta import relativedelta
except:
    print("please verify that the following packages installed: dateutil\n if not you can install it by running  python -m pip install dateutil")
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
    return values

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
filename = str("unique_users_in_org_result_for-"+current_time)
sumnum = 0
csvname=filename+".csv"

#creating pretty table for adding row by the end of each run
monthnames=getmonthnames()
firststep=["Org Name"]
laststep=["current named users in org"]
coloumns=firststep+monthnames+laststep
prettyT = PrettyTable(coloumns)
prettyT.align["Org Name"] = "l" # Left align city names
prettyT.padding_width = 1 # One space between column edges and contents (default)

#starting to call the functions and writing the csv file line by line
with open(csvname, 'a+', newline='') as write_obj:
    # Create a writer object from csv module
    csv_writer = csv.writer(write_obj)
    csv_writer.writerow(coloumns)
    try:
            #opening orgs list file if suppllied and calling the functions if failed will proceed to except
            with open(ORGS_LIST_PATH, "r") as a_file:
                for line in a_file:
                    stripped_line = line.strip()
                    EORG=stripped_line
                    print("working on: " + EORG)
                    token = get_access_token()
                    lastnum = uniqueUsers()
                    totalusers = userscount()
                    try:
                        sumrow = sum(lastnum)
                        sumnum += sum(lastnum)
                        fulllmonthnum=create_laswithdate(lastnum)
                    except:
                        sumrow = int(lastnum)
                        tmpnum= int(lastnum)
                        sumnum+=sumrow
                    lastnum=fulllmonthnum
                    fulllmonthnum = str(lastnum)[1:-1]
                    totalusers = str(totalusers)
                    #print( EORG + "," + time + ", " + fulllmonthnum + "," + totalusers)
                    a=[EORG]
                    b=[totalusers]
                    towrite= a + lastnum + b
                    #print(towrite)
                    csv_writer.writerow(towrite)
                    prettyT.add_row(towrite)
    except:
        print("file content not found")
        EORG = input("Please enter org name:\n")
        token = get_access_token()
        lastnum = uniqueUsers()
        totalusers = str(userscount())
        try:
            sumrow = sum(lastnum)
            sumnum += sum(lastnum)
            fulllmonthnum = create_laswithdate(lastnum)
        except:
            sumrow = int(lastnum)
            tmpnum = int(lastnum)
            sumnum += sumrow
        lastnum = fulllmonthnum
        fulllmonthnum = str(lastnum)[1:-1]
        #print(EORG + "," + time + ", " + fulllmonthnum + "," + totalusers)
        a = [EORG]
        b = [totalusers]
        towrite = a + lastnum + b
        #print(towrite)
        #writing to the csv and pretty table
        csv_writer.writerow(towrite)
        prettyT.add_row(towrite)

#counting the number of coloumns need to be created
clolumnslen=len(towrite)-3
firststep=["sum connected users"]
emptylist=[""]
emptycol=emptylist*clolumnslen
total=firststep+emptycol+[sumnum]+emptylist
#prettyT.add_row(total)
#printing data to users screen
print("done")
print("\n"+prettyT.get_string(title="Monthly Users connectivity statistics"))
with open("%s.prettytable" %filename, 'w') as write_obj:
    write_obj.write(str(prettyT.get_string(title="Monthly Users connectivity statistics")))
print("\nfiles has been saved successfully.\nas csv format: " + filename + "\nas a table: " + filename + ".prettytable" )
#print("sum number of all orgs in script (sum of all months): " + str(sumnum))
exit()