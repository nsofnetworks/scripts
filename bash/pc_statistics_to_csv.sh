#!/bin/bash

#this script will provide the option to get statistics regarding failed posture check attempt

#Please fill the path to the API before running the script (only csv or txt file)
API_KEY="Path/to/the/API/Key/file"
API_ID="Path/to/the/API/ID/file"
#Sub_Org is Optional, not optional for MSSP
Sub_ORG="Path/to/the/Sub/ORG/file"

if [ "$1" == "-h" ] || [ "$1" == "--help" ]; then
  echo "Usage: `basename $0` filename.csv "
  exit 0
fi

trap 'rm pc-temp-stat temp01 ' INT

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

#choosing number of days
from=$(date +'%Y-%m-%d' -d '-0 days')
to=$(date +'%Y-%m-%d')
fileName=$(echo $org &date +'%Y-%m-%d.%T' | sed 's/:/-/g')
fileName=$(echo "posture_check_statistics_"$fileName | sed 's/ /./g')

echo "posture check statistics between $from to $to" > $fileName.csv
echo "name,id,failed attempts,success,total,percentage of failed attempts, percentage of success attempts" >> $fileName.csv

echo "starting to download data"
#curl get request to download the necessery content from security logs, then perform jq filtering command to get only necessery data
offs=0
res=2500
Url="https://api.metanetworks.com/v1/audit/security?limit=2500&offset="$offs"&time_from="$from"T00:00:01.00Z&time_to="$to"T23:59:59.00Z""&events=posture_check"
echo $Url
curl -X GET "$Url" -H "Authorization: Bearer $token" > temp01
countmax=$(cat temp01 | jq .max_count)
echo "this is countmax: $countmax"
cat temp01 | jq .'[] | .[] | [.caller_id, .caller_name, .timestamp], (.context | .report | .[] | [.id, .name, .pass]) | @csv' | sed 's/"//g' | sed 's/\\//g' > pc-temp-stat
rm temp01

#donwloading data with number offsets as needed
while [ $countmax -gt $res ];do
offs=$(expr $offs + 2500)
Url="https://api.metanetworks.com/v1/audit/security?limit=2500&offset="$offs"&time_from="$from"T00:00:01.00Z&time_to="$to"T23:59:59.00Z""&events=posture_check"
curl -X GET "$Url" -H "Authorization: Bearer $token" | jq .'[] | .[] | [.caller_id, .caller_name, .timestamp], (.context | .report | .[] | [.id, .name, .pass]) | @csv' | sed 's/"//g' | sed 's/\\//g' >> pc-temp-stat
res=$(expr $res + 2500)
done;

echo "calculatig statistics"
#calculating the number of failed attempts per posture check
for i in $(cat pc-temp-stat | grep -e "pc-" | cut -f1 -d"," | sort -u); do sumfailed=$(cat pc-temp-stat | grep $i | grep false | wc -l);sumsuccess=$(cat pc-temp-stat | grep $i | grep true | wc -l);sumtotal=$(cat pc-temp-stat | grep $i | wc -l);name=$(cat pc-temp-stat | grep $i | cut -d"," -f2|sort -u);failedpercetage=$( awk -vn=$sumfailed -vt=$sumtotal  'BEGIN{print(n/t*100)}');successpercentage=$(awk -vn=$sumsuccess -vt=$sumtotal  'BEGIN{print(n/t*100)}');sumallfailed=$(expr $sumallfailed + $sumfailed);sumallsuccess=$(expr $sumallsuccess + $sumsuccess);sumalltotal=$(expr $sumalltotal + $sumtotal);echo "$name,$i,$sumfailed,$sumsuccess,$sumtotal,$failedpercetage%,$successpercentage%" >> $fileName.csv;done

#writing the total of total
totalfailedpercentage=$(awk -vn=$sumallfailed -vt=$sumalltotal  'BEGIN{print(n/t*100)}')
totalsuccesspercentage=$(awk -vn=$sumallsuccess -vt=$sumalltotal  'BEGIN{print(n/t*100)}')
echo "total,,$sumallfailed,$sumallsuccess,$sumalltotal,$totalfailedpercentage%,$totalsuccesspercentage%" >> $fileName.csv

echo "" >>$fileName.csv
echo "" >>$fileName.csv

#writing all logs to a CSV file
echo "writing the logs to a CSV file"
echo "id,name,time,pass" >> $fileName.csv
cat pc-temp-stat | while IFS=$',' read -r id name time;do firstchar=$(echo $id | head -c 1);if [ "$firstchar" == "u" ];then echo "$id,$name,$time" >> $fileName.csv;elif [ "$firstchar" == "p" ];then echo ",$id,$name,$time" >> $fileName.csv;fi;done

echo "file has been saved has $fileName.csv"
rm pc-temp-stat
echo "done"
