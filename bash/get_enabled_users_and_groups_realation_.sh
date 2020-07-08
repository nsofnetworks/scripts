#!/bin/bash
#version 1.2
#Please fill the path to the API before running the script (only csv or txt file)
API_KEY="Path/to/the/API/Key/file"
API_ID="Path/to/the/API/ID/file"
#Sub_Org is Optional, not optional for MSSP
Sub_ORG="Path/to/the/Sub/ORG/file"

if [ "$1" == "-h" ] || [ "$1" == "--help" ]; then
  echo "Usage: `basename $0` filename.csv "
  echo "script version 1.2"
  exit 0
fi

trap 'rm tempUsers tempUsers2 tempGroups22' INT

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

echo "Email,Family Name, Private Name,Groups,Role" > $1
curl -X GET https://api.metanetworks.com/v1/users -H "Content-Type: application/json" -H "Authorization: Bearer $token" > tempUsers2
cat tempUsers2 | jq -r '.[] | select (.enabled=='true') | .email, .family_name, .given_name, .id' > tempUsers
curl -X GET https://api.metanetworks.com/v1/groups?expand=true -H "Content-Type: application/json" -H "Authorization: Bearer $token" > tempGroups22 


while IFS= read -r field1; do
	((l = l+1))
	groups2=""
	if [ $l -eq 1 ]; then  
	email=$field1
	email2="$email"
	continue
	fi
	if [ $l -eq 2 ]; then 
	family_name=$field1
	continue
	fi
	if [ $l -eq 3 ]; then 
	private_name=$field1
	role=$(cat tempUsers2 | jq -r --arg email2 "$email2" '.[] | select (.email==$email2) | .roles' ) && role="${role::-1}" && role="${role#?}" && role="${role//,}"
	role=`echo $role | sed 's/\\r//g'`
	continue
	fi	
	if [ $l -eq 4 ]; then 
	id=$field1
	groups2=$(cat tempGroups22 | jq --arg id "$id" .' | .[] | select (.users|.[]==$id) | .name' | sed 's/"//g')
	echo ""
	echo ""
	echo "Writing the user:" $id
	str=$email,$family_name,$private_name,$groups2,$role
	echo $str >> $1
	l=0
	echo $str
	continue
	fi
	
done < tempUsers

rm tempUsers tempUsers2 tempGroups22