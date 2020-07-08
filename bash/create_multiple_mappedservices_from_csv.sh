#!/bin/bash

#version = 1.1
#Please fill the path to the API before running the script (only csv or txt file)
API_KEY="Path/to/the/API/Key/file"
API_ID="Path/to/the/API/ID/file"
#Sub_Org is Optional, not optional for MSSP
Sub_ORG="Path/to/the/Sub/ORG/file"

if [ "$1" == "-h" ] || [ "$1" == "--help" ]; then
  echo "Usage: `basename $0` filename.csv API-ID API-key "
  echo "File format should be as following: ServiceName,Description(optional),IP\Hostname,Aliase(optional),MPID"
  echo "note:verify the file dosen't habe spaces"
  echo "script version 1.1"
  exit 0
fi

trap 'rm tempelements' INT

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
	
while IFS=, read -r field1 field2 field3 field4 field5
do
Name=$field1
Description=$field2
IP=$field3
PreAliase=$field4
MPID=$field5

echo "creating mapped service details: $Name $Description $IP $PreAliase $MPID"
Aliase=/aliases/$PreAliase


if [ -z $Description ]; then
	firstJson='{"name": "'"$Name"'", "mapped_service": "'"$IP"'"}'
else
	firstJson='{"name": "'"$Name"'", "mapped_service": "'"$IP"'", "description": "'"$Description"'"}'
fi

#uncomment those lines if the csv file as a lot services (refresh token)

# #if using sub org so use different string
# if [ -z $org ]; then
# token=$(curl -d '{"grant_type":"client_credentials", "client_id":"'"$id"'", "client_secret":"'"$key"'"}' -H "Content-Type: application/json" -X POST https://api.metanetworks.com/v1/oauth/token | jq -r ".access_token")
# else
# token=$(curl -d '{"grant_type":"'"client_credentials"'", "client_id":"'"$id"'", "client_secret":"'"$key"'", "scope": "'"org:$org"'"}' -H "Content-Type: application/json" -X POST https://api.metanetworks.com/v1/oauth/token | jq -r ".access_token")
# fi

NEID=$(curl -X POST https://api.metanetworks.com/v1/network_elements -H "Authorization: Bearer $token" -H "Content-Type: application/json" "-d $firstJson" | jq -r ".id")

if [ -z $field4 ]; then
	echo "no Aliase"
else
	firstURL=https://api.metanetworks.com/v1/network_elements/
	URL1=$firstURL$NEID$Aliase
	aliaseURL=$(curl -X PUT "$firstURL$NEID$Aliase" -H "Authorization: Bearer $token" -H "Content-Type: application/json")
fi

AFTER2=`echo $MPID | sed 's/\\r//g'`
tempelementsFIle=$(curl -X GET "https://api.metanetworks.com/v1/metaports" -H "Authorization: Bearer $token" -H "Content-Type: application/json" > tempelements)

AFTER2=`echo $MPID | sed 's/\\r//g'`
string="jq .'[] | select (.id =="'"${AFTER2}"'") | .mapped_elements'"
MPElements=$(jq .'[] | select (.id =="'"${AFTER2}"'") | .mapped_elements' tempelements)

MPElements2=$(jq .'[] | select (.id =="'"${AFTER2}"'") | .mapped_elements' tempelements)
MPElements2="${MPElements2::-1}"
MPElements2=${MPElements2#?};

rm tempelements

if [ -z "$MPElements2" ]; then
	echo "attached the first resource to this MP"
	newElements="${MPElements::-1}"
	editeElements=$newElements'"'$NEID'"']
	echo "this is null, edit.." $editeElements
else
	echo "attached a MP for the resource"
	newElements="${MPElements::-1}"
	editeElements=$newElements,'"'$NEID'"']
fi

secURL=https://api.metanetworks.com/v1/metaports/
secJson='{"mapped_elements": '$editeElements'}'

URL=$secURL$MPID
AFTER=`echo $URL | sed 's/\\r//g'`
patchedMP=$(curl -X PATCH "$AFTER" -H "Authorization: Bearer $token" -H "Content-Type: application/json" "-d $secJson")

done < $1
