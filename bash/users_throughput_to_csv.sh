#!/bin/bash

#This script will provide the option to recieve a csv file with the 100 top users by throughput for organization

#Please fill the path to the API before running the script (only csv or txt file)
#API Secret
API_KEY="Path/to/the/API/Key/file"

#API Key ID
API_ID="Path/to/the/API/ID/file"

#Sub_Org is Optional
Sub_ORG="Path/to/the/Sub/ORG/file"

if [ "$1" == "-h" ] || [ "$1" == "--help" ]; then
  echo "Usage: `basename $0` filename.csv "
  exit 0
fi

trap 'rm $fileName.users $fileName.temp_values' INT

checkJq=$(which jq)
if [ -z $checkJq ]; then
	echo "please install jq before running the script"
	exit 0
else
	echo "jq path:" $checkJq
fi

if [ -z $API_ID ] || [ -z $API_ID ]; then
	echo "please edit the script and paste the path to the API_Key and API_ID files (2 first lines in the script)"
	exit 0
else
	key=$(head -n 1 $API_KEY)
	id=$(head -n 1 $API_ID)
	key=`echo $key | sed 's/\\r//g'`
	id=`echo $id | sed 's/\\r//g'`
fi

origSUB_ORG="Path/to/the/Sub/ORG/file"
if [ $Sub_ORG == $origSUB_ORG ] || [ -z $Sub_ORG ]; then
	echo "sub org didn't configured"
else
	org=$(head -n 1 $Sub_ORG)
	org=`echo $org | sed 's/\\r//g'`
fi

echo ""
echo "" 
echo "Please select the number of days you would like to receive the report ( between 1 to 30 days):"

read menu

while [[ -n ${menu//[0-9]/} ]] || [ $menu -lt 1 ] || [ $menu -gt 30 ] ; do
if [[ -n ${menu//[0-9]/} ]]; then
    echo "your input contains illegal charcter"
fi
echo "the selected number isn't between 1 to 30"
echo "Please select the number of days you would like to receive the report again:"
read menu
done

#if using sub org so use different string
if [ -z $org ]; then
token=$(curl -d '{"grant_type":"client_credentials", "client_id":"'"$id"'", "client_secret":"'"$key"'"}' -H "Content-Type: application/json" -X POST https://api.metanetworks.com/v1/oauth/token | jq -r ".access_token")
else
token=$(curl -d '{"grant_type":"'"client_credentials"'", "client_id":"'"$id"'", "client_secret":"'"$key"'", "scope": "'"org:$org"'"}' -H "Content-Type: application/json" -X POST https://api.metanetworks.com/v1/oauth/token | jq -r ".access_token")
fi

#verify that the token\key\id isn't null
if [ -z $token ] || [ -z $key ] || [ -z $id ] || [ $token == null ]; then
	echo "please verify the path to API_KEY and API_ID files or the Key\ID"
	exit 0
else 
	echo "your token is:" $token
	echo "note:you can verify the token permissions and the org id by decoding the token string as base 64"
fi


fileName=$(echo $org &date +'%Y-%m-%d.%T' | sed 's/:/-/g')
fileName=$(echo "users_throughput_"$fileName | sed 's/ /./g')

echo "throughput statistics for top 100 users over the last $menu day\s" > $fileName.csv
echo "" >> $fileName.csv
echo "id,name,MB,GB" >> $fileName.csv
from=$(date +'%Y-%m-%d' -d "-$menu days")
to=$(date +'%Y-%m-%d')

#create URL and run 2 requests to /users and /metric/top/users"
echo ""
echo "downloading users throughput"
Url="https://api.metanetworks.com/v1/metrics/top/users?time_from="$from"T0:01:00.00Z&time_to="$to"T00:01:00.00Z&limit=100"
curl -X GET "$Url" -H "Authorization: Bearer $token" | jq '.[]|.[]|.[]| [.key, .value] | @csv' > $fileName.temp_values
echo ""
echo "downloading users details"
curl -X GET https://api.metanetworks.com/v1/users -H "Content-Type: application/json" -H "Authorization: Bearer $token" > $fileName.users

echo "writing information to file"
cat $fileName.temp_values | while IFS=$',' read -r id throughput;do id=$(echo $id | sed 's/\\"//g' | sed 's/"//g' ); name=$(cat $fileName.users | jq --arg id "$id" .'[] | select (.id==$id) | .name' | sed 's/\\"//g' | sed 's/"//g');throughput=$(echo $throughput | sed 's/"//g' );
#Convert bytes to MB,GB
call_bc() {
 n1=$throughput
 n2=$2
 echo "scale=4; $n1/($n2)" |bc
}
nm=$throughput
pw=$2
pn=""
k_ilo=1024;
m_ega=$k_ilo*$k_ilo;
g_iga=$m_ega*$k_ilo;
[ -z "$nm" ] && exit

for i in MB GB ; do
 case $i in
  MB) let pn=$m_ega;;
  GB) let pn=$g_iga;;
 esac
 sum=$(call_bc $nm $pn)
 if [ "$i" == "MB" ];then MB=$sum
 elif [ "$i" == "GB" ];then GB=$sum;fi
done; 

#writing data to csv file
echo $id,$name,$MB,$GB >> $fileName.csv ;done

echo "file has been saved has $fileName.csv"
rm $fileName.users $fileName.temp_values
echo "done"

