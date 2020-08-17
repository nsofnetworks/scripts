import os
import sys
import subprocess
import pkg_resources
import pprint
import csv
import argparse

'''This script will provide the option to create multiple users that has been writen in a csv file
the csv file format should be as following: email,description,family name,first name,phone (optional)

reading the API keys has 2 options (file,env variables),by default the script will try to read from file and if not defined it will
proceed to read from environemnt varaibles:

reading from file:
Please fill the path to API_KEY_ID_PATH and API_KEY_SECRET_PATH before running the script (only csv or txt file)
Example: "C:\\Users\\administrator\\Desktop\\ID.csv"

reading from env variables:
the varaibles should be added as the following:
API_KEY_ID = value
API_KEY_SECRET = value
'''

API_KEY_ID_PATH = "Replace this text with the path to the API ID file"
API_KEY_SECRET_PATH = "Replace this text with the path to the API secret file"
CREATE_USERS_CSV = "Replace this text with the path to the CSV file"

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
except:
    print(
        "please verify the path to API_KEY_ID and API_KEY_SECRET or your env variables and also that the key is valid with write privilege"
        "to users")
    exit()

# function to get access token
def get_access_token():
    url = "%s/v1/oauth/token" % API_ENDPOINT
    try:
        request_data = {"grant_type": "client_credentials",
                        "client_id": API_KEY_ID,
                        "client_secret": API_KEY_SECRET}

        response = requests.post(url=url, json=request_data)
        response.raise_for_status()
        return response.json()['access_token']
    except:
        print("please verify the path to API_KEY_ID and API_KEY_SECRET and also that the key is valid with write "
              "privilege to users")
        exit()


if __name__ == '__main__':
    pp = pprint.PrettyPrinter(indent=4)
    token = get_access_token()


# create user function
def create_user(access_token, email, description, family_name, first_name, phone=""):
    url = "%s/v1/users" % API_ENDPOINT
    headers = {'Authorization': 'Bearer %s' % access_token}
    if phone == "":
        body = {'email': email,
                'description': description,
                'family_name': family_name,
                'given_name': first_name,
                }
    else:
        body = {'email': email,
                'description': description,
                'family_name': family_name,
                'given_name': first_name,
                'phone': phone,
                }
    response = requests.post(url=url, json=body, headers=headers)
    return response.json()
    print(response)


# reading from CSV file
try:
    with open(CREATE_USERS_CSV, newline='') as csvFile:
        csvRead = csv.reader(csvFile, delimiter=',', quotechar='|')
        try:
            for row in csvRead:
                email = row[0]
                description = row[1]
                family_name = row[2]
                first_name = row[3]
                if len(row) > 4 and row[4] == "" or row[4] == '"':
                    create_user_params = create_user(token, email, description, family_name, first_name)
                    pp.pprint(create_user_params)
                else:
                    if row[-1] == "":
                        row[:-1]
                        row[:-1]
                    phonenumber = row[4]
                    create_user_params = create_user(token, email, description, family_name, first_name, phonenumber)
                    pp.pprint(create_user_params)
        except AssertionError as error:
            print(error)
            print('failed while creating the user:', email)
            exit()

except:
    print("can not read from CSV file, please verify the path and that the CSV is is the following format:email,"
          "description,family name,first name,phone (optional)")
    exit()

print('done')
exit()