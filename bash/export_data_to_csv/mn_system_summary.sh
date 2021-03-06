#!/bin/bash
#this script is providing the option to export the following data into CSV file"
# Active users last 30 days - Minimum,Average,Maximum
# Roles - ID,Name,Role
# MetaPorts - ID,Name,Enabled,Mapped Elements
# Mapped Subnets - ID,Name,CIDR,DNS Suffix:Enterprise DNS (true\flase),Host Name
# Mapped service - ID,Name,IP\HostName,DNS Suffix
# Policies - ID,Name,Created at,Description,Enabled,Modified at,Sources,Target,Protocols
# Egress ID,Name,Source,Target,Via
# Routing Groups - ID,Name,Mapped elements,Sources
# Easy Links - ID,Name,Mapped elements,Domain name,IP/HostName (null=probably it's subnet),Port,Protocol,Viewers
# Split Tunnel Configuration - ID,Name,All org,Members
# IDPS - ID,Name,Created at,Modified at,SAML,SCIM key (if defined)
# Log Streaming - ID,Name,SIEM Configuration (URL:Port:Protocol)
# All data above

# version = 1.5
# Please fill the path to the API before running the script (only csv or txt file)
API_KEY="Path/to/the/API/Key/file"
API_ID="Path/to/the/API/ID/file"
#Sub_Org is Optional, not optional for MSSP
Sub_ORG="Path/to/the/Sub/ORG/file"


if [ "$1" == "-h" ] || [ "$1" == "--help" ]; then
  echo "the script will provide the following information:
1.Active users last 30 days - Minimum,Average,Maximum
2.Roles - ID,Name,Role
3.MetaPorts - ID,Name,Enabled,Mapped Elements
4.Mapped Subnets - ID,Name,CIDR,DNS Suffix:Enterprise DNS (true\flase),Host Name
5.Mapped service - ID,Name,IP\HostName,DNS Suffix
6.Policies - ID,Name,Created at,Description,Enabled,Modified at,Sources,Target,Protocols
7.Egress ID,Name,Source,Target,Via
8.Routing Groups - ID,Name,Mapped elements,Sources
9.Easy Links - ID,Name,Mapped elements,Domain name,IP/HostName (null=probably it's subnet),Port,Protocol,Viewers
10.Split Tunnel Configuration - ID,Name,All org,Members
11.IDPS - ID,Name,Created at,Modified at,SAML,SCIM key (if defined)
12.Log Streaming - ID,Name,SIEM Configuration (URL:Port:Protocol)
100.All data above

0.Exit

Examples: `basename $0`

script version 1.5"
  exit 0
fi

trap 'rm idps.$org.csv $org.routing_groups $org.EasyLinks $org.Network_Elements $org.Device_Settings $org.MP $org.Access.Bridge $org.policies $org.groups $org.protocol_groups $org.roles $org.users $org.active.users &> /dev/null' INT

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


echo ""
echo "" 
echo "Please select which data would you like to export
1.Active users last 30 days - Minimum,Average,Maximum
2.Roles - ID,Name,Role
3.MetaPorts - ID,Name,Enabled,Mapped Elements
4.Mapped Subnets - ID,Name,CIDR,DNS Suffix:Enterprise DNS (true\flase),Host Name
5.Mapped service - ID,Name,IP\HostName,DNS Suffix
6.Policies - ID,Name,Created at,Description,Enabled,Modified at,Sources,Target,Protocols
7.Egress ID,Name,Source,Target,Via
8.Routing Groups - ID,Name,Mapped elements,Sources
9.Easy Links - ID,Name,Mapped elements,Domain name,IP/HostName (null=probably it's subnet),Port,Protocol,Viewers
10.Split Tunnel Configuration - ID,Name,All org,Members
11.IDPS - ID,Name,Created at,Modified at,SAML,SCIM key (if defined)
12.Log Streaming - ID,Name,SIEM Configuration (URL:Port:Protocol)
100.All data above

0.Exit"

read menu

if [ "$menu" == "0" ]; then
exit 0
fi

if [ -z "$org" ];then
echo "Please type your org name:"
read org
fi


if [ "$menu" == "100" ] || [ "$menu" == "6" ] ; then
curl -X GET https://api.metanetworks.com/v1/policies -H "Content-Type: application/json" -H "Authorization: Bearer $token" > $org.policies
fi
if [ "$menu" == "100" ] || [ "$menu" == "6" ] || [ "$menu" == "4" ]; then
curl -X GET https://api.metanetworks.com/v1/groups -H "Content-Type: application/json" -H "Authorization: Bearer $token" > $org.groups
fi
if [ "$menu" == "100" ] || [ "$menu" == "6" ]; then
curl -X GET https://api.metanetworks.com/v1/protocol_groups -H "Content-Type: application/json" -H "Authorization: Bearer $token" > $org.protocol_groups
fi
if [ "$menu" == "100" ] || [ "$menu" == "11" ]; then
curl -X GET https://api.metanetworks.com/v1/settings/idps -H "Content-Type: application/json" -H "Authorization: Bearer $token" >idps.$org.csv
fi
if [ "$menu" == "100" ] || [ "$menu" == "8" ]; then
curl -X GET https://api.metanetworks.com/v1/routing_groups -H "Content-Type: application/json" -H "Authorization: Bearer $token" > $org.routing_groups
fi
if [ "$menu" == "100" ] || [ "$menu" == "9" ]; then
curl -X GET https://api.metanetworks.com/v1/easylinks -H "Content-Type: application/json" -H "Authorization: Bearer $token" > $org.EasyLinks
fi
if [ "$menu" == "100" ] || [ "$menu" == "9" ] || [ "$menu" == "6" ] || [ "$menu" == "5" ] || [ "$menu" == "9" ] || [ "$menu" == "4" ]; then
curl -X GET https://api.metanetworks.com/v1/network_elements?expand=true -H "Content-Type: application/json" -H "Authorization: Bearer $token" > $org.Network_Elements
fi
if [ "$menu" == "100" ] || [ "$menu" == "10" ]; then
curl -X GET https://api.metanetworks.com/v1/settings/device -H "Content-Type: application/json" -H "Authorization: Bearer $token" > $org.Device_Settings
fi
if [ "$menu" == "100" ] || [ "$menu" == "3" ]; then
curl -X GET https://api.metanetworks.com/v1/metaports -H "Content-Type: application/json" -H "Authorization: Bearer $token" > $org.MP
fi
if [ "$menu" == "100" ] || [ "$menu" == "12" ]; then
curl -X GET https://api.metanetworks.com/v1/access_bridges -H "Content-Type: application/json" -H "Authorization: Bearer $token" > $org.Access.Bridge
fi
if [ "$menu" == "100" ] || [ "$menu" == "2" ]; then
curl -X GET https://api.metanetworks.com/v1/roles -H "Content-Type: application/json" -H "Authorization: Bearer $token"  > $org.roles
fi
if [ "$menu" == "100" ] || [ "$menu" == "1" ] || [ "$menu" == "4" ] || [ "$menu" == "2" ] || [ "$menu" == "6" ]; then
curl -X GET https://api.metanetworks.com/v1/users -H "Content-Type: application/json" -H "Authorization: Bearer $token" > $org.users
fi
if [ "$menu" == "100" ] || [ "$menu" == "7" ]; then
curl -X GET https://api.metanetworks.com/v1/egress_routes -H "Content-Type: application/json" -H "Authorization: Bearer $token" > $org.Egress
fi

fileName=$(echo $org &date +'%Y-%m-%d.%T' | sed 's/:/-/g')
fileName=$(echo $fileName | sed 's/ /./g')

echo "$org" > $fileName.csv
echo "" >> $fileName.csv

if [ "$menu" == "100" ] || [ "$menu" == "1" ]; then
	
#URL for users time 
from=$(date +'%Y-%m-%d' -d '-30 days')
to=$(date +'%Y-%m-%d')
Url="https://api.metanetworks.com/v1/metrics/unique/users/daily?time_from="$from"T0:01:00.00Z&time_to="$to"T00:01:00.00Z"
curl -X GET "$Url" -H "Authorization: Bearer $token" > $org.active.users



#Active users last 30 days
echo "calculating the number of active users during the last 30 days"
echo "" >> $fileName.csv
echo "Number of active between ($from to: $to)" >> $fileName.csv
echo "Minimum,Average,Maximum" >> $fileName.csv

Max=$(cat $org.active.users  | jq .'users_count | .[] | ."value"' | sort -rn | head -n 1)
Average=$(cat $org.active.users  | jq .'users_count | .[] | ."value"' | awk '{s+=$1} END {print s/NR}')
Average=$(echo $Average | cut -f1 -d".")
Min=$(cat $org.active.users| jq .'users_count | .[] | ."value"' | sort -rn | tail -n 1)

echo "$Min,$Average,$Max" >> $fileName.csv
fi
if [ "$menu" == "100" ] || [ "$menu" == "2" ]; then
#Roles
echo "writing Roles"
echo "" >> $fileName.csv
echo "" >> $fileName.csv
echo "" >> $fileName.csv
echo "Roles" >> $fileName.csv
echo "ID,Name,Role" >> $fileName.csv

cat $org.users | jq .'[] | [.id, .name, (.roles | .[])] | @csv' | sed 's/\\//g' | sed 's/"//g' | awk -F , 'NF > 2' | sed 's/,.*//g'| while iFS= read id; do roleName="";name=$( cat $org.users | jq --arg id "$id" .'[] | select (.id==$id) | .name' | sed 's/"//g');for i in $(cat $org.users | jq --arg id "$id" .'[] | select (.id==$id) | .roles | .[]' | sed 's/\\//g' | sed 's/"//g' ); do tempName=$(cat $org.roles | jq --arg i "$i" .'[] | select (.id==$i) | [.name] |@csv' | sed 's/.$/ /' |sed 's/\\//g' | sed 's/,//g' |sed 's/"//g');roleName+=$tempName;done; echo $id,$name,$roleName >> $fileName.csv;done;
fi

if [ "$menu" == "100" ] || [ "$menu" == "3" ]; then
#Meta Ports
echo "" >> $fileName.csv
echo "" >> $fileName.csv
echo "" >> $fileName.csv
echo "Meta Ports " >> $fileName.csv
echo "ID,Name,Enabled,Mapped Elements" >> $fileName.csv
echo "writing Meta Ports"
cat $org.MP | jq .'[] | [.name, .id, .enabled] | @csv' | while IFS=$',' read -r name id enabled; do id=$(echo $id | sed 's/\\//g' | sed 's/"//g'); Mapped_elements=$(cat $org.MP | jq --arg id "$id" .'[] | select (.id==$id) | [.mapped_elements | .[]] | @csv' | sed 's/\\//g' | sed 's/,/ /g' | sed 's/"//g');echo $id,$name,$enabled,$Mapped_elements | sed 's/\\//g' | sed 's/"//g' >> $fileName.csv;done;

fi

if [ "$menu" == "100" ] || [ "$menu" == "4" ]; then
Find_Name_source () {
for i in $(cat $org.policies | jq -r --arg id "$id" '.[] | select (.id==$id) | [.sources] | .[] | @csv' | sed 's/"//g');do firstChars=$(echo $i | cut -c1-2); if [ "$firstChars" == "gr" ]; then sourceTemp=$(cat $org.groups | jq -r --arg i "$i" .'[] | select (.id==$i) | .name');source+="$sourceTemp-" ;
elif  [ "$firstChars" == "us" ];then  
sourceTemp=$(cat $org.users | jq -r --arg i "$i" .'[] | select (.id==$i) | .name');source+="$sourceTemp-";
elif  [ "$firstChars" == "ne" ];then  
sourceTemp=$(cat $org.Network_Elements | jq -r --arg i "$i" .'[] | select (.id==$i) | .name');source+="$sourceTemp-";
fi;
done;
}

Find_Name_target () {
for i in $(cat $org.policies | jq -r --arg id "$id" '.[] | select (.id==$id) | [.destinations] | .[] | @csv' | sed 's/"//g');do firstChars=$(echo $i | cut -c1-2);
if [ "$firstChars" == "gr" ]; then targetTemp=$(cat $org.groups | jq -r --arg i "$i" .'[] | select (.id==$i) | .name');target+="$targetTemp-" ;
elif  [ "$firstChars" == "us" ];then  
targetTemp=$(cat $org.users | jq -r --arg i "$i" .'[] | select (.id==$i) | .name');target+=";$targetTemp-";
elif  [ "$firstChars" == "ne" ];then targetTemp=$(cat $org.Network_Elements | jq -r --arg i "$i" .'[] | select (.id==$i) | .name');target+=";$targetTemp-";
fi;
done;
}


#Mapped Subnets 
echo "" >> $fileName.csv
echo "" >> $fileName.csv
echo "" >> $fileName.csv
echo "Mapped Subnets" >> $fileName.csv
echo "ID,Name,CIDR,DNS Suffix:Enterprise DNS (true\flase),Host Name," >> $fileName.csv
echo "writing Mapped Subnets"
 DNS_Seperate () {
   DNS=$(cat $org.Network_Elements | jq --arg id "$id" .'[] | select (.id==$id) | .mapped_domains | .[] | [.mapped_domain, .name ,.enterprise_dns] | @csv' | sed 's/"//g' | sed 's/,/>>/' | sed 's/\\//g' | sed 's/,/:/g');
 }

 cat $org.Network_Elements | jq .'[] | select (.type=="Mapped Subnet") | [.name, .id] | @csv' | while IFS=$',' read -r name id; do name=$(echo $name | sed 's/"//g' | sed 's/\\//g'); id=$(echo $id | sed 's/\\"//g' | sed 's/"//g' ); CIDR=$(cat $org.Network_Elements | jq --arg id "$id" .'[] | select (.id==$id) | [ .mapped_subnets | .[]] | @csv' | sed 's/\\//g' | sed 's/,//g' | sed 's/"/ /g'); Host=$(cat $org.Network_Elements | jq --arg id "$id" .'[] | select (.id==$id) | .mapped_hosts | .[] | [.mapped_host, .name] | @csv' | sed 's/\\//g' | sed 's/"//g' | sed 's/,/:/g');DNS_Seperate "$id"; echo $id,$name,$CIDR,$DNS,$Host >> $fileName.csv; done;
fi

if [ "$menu" == "100" ] || [ "$menu" == "5" ]; then
#Mapped Service
echo "writing Mapped Services"
echo "" >> $fileName.csv
echo "" >> $fileName.csv
echo "" >> $fileName.csv
echo "Mapped Services" >> $fileName.csv
echo "ID,Name,IP\HostName,DNS Suffix" >> $fileName.csv

cat $org.Network_Elements | jq .'[] | select (.type=="Mapped Service") | [.name, .id, .mapped_service] | @csv' | while IFS=$',' read -r name id mapped_service; do id=$(echo $id | sed 's/\\"//g' | sed 's/"//g' ); aliases=$(cat $org.Network_Elements | jq --arg id "$id" .'[] | select (.id==$id) | [.aliases | .[]] | @csv' | sed 's/"//g' | sed 's/,/ /g'); echo $name,$id,$mapped_service,$aliases | sed 's/\\//g' | sed 's/"//g' >> $fileName.csv;done;

fi

if [ "$menu" == "100" ] || [ "$menu" == "6" ]; then

Find_Name_source () {
for i in $(cat $org.policies | jq -r --arg id "$id" '.[] | select (.id==$id) | [.sources] | .[] | @csv' | sed 's/"//g');do firstChars=$(echo $i | cut -c1-2); if [ "$firstChars" == "gr" ]; then sourceTemp=$(cat $org.groups | jq -r --arg i "$i" .'[] | select (.id==$i) | .name');source+="$sourceTemp-" ;
elif  [ "$firstChars" == "us" ];then  
sourceTemp=$(cat $org.users | jq -r --arg i "$i" .'[] | select (.id==$i) | .name');source+="$sourceTemp-";
elif  [ "$firstChars" == "ne" ];then  
sourceTemp=$(cat $org.Network_Elements | jq -r --arg i "$i" .'[] | select (.id==$i) | .name');source+="$sourceTemp-";
fi;
done;
}

Find_Name_target () {
for i in $(cat $org.policies | jq -r --arg id "$id" '.[] | select (.id==$id) | [.destinations] | .[] | @csv' | sed 's/"//g');do firstChars=$(echo $i | cut -c1-2);
if [ "$firstChars" == "gr" ]; then targetTemp=$(cat $org.groups | jq -r --arg i "$i" .'[] | select (.id==$i) | .name');target+="$targetTemp-" ;
elif  [ "$firstChars" == "us" ];then  
targetTemp=$(cat $org.users | jq -r --arg i "$i" .'[] | select (.id==$i) | .name');target+=";$targetTemp-";
elif  [ "$firstChars" == "ne" ];then targetTemp=$(cat $org.Network_Elements | jq -r --arg i "$i" .'[] | select (.id==$i) | .name');target+=";$targetTemp-";
fi;
done;
}

#policies
echo "working on ploicies"
echo "" >> $fileName.csv
echo "" >> $fileName.csv
echo "" >> $fileName.csv
echo "Policies" >> $fileName.csv

echo "ID,Name,Created at,Description,Enabled,Modified at,Sources,Target,Protocols" >> $fileName.csv
cat $org.policies | jq .'[] | [.id, .name, .created_at, .description, .enabled, .modified_at] | @csv' | sed 's/\\//g' | sed 's/"//g' | while IFS=$"," read -r id name created_at description enabled modified_at; do proto=""; PG=$(cat $org.policies | jq -r --arg id "$id" '.[] | select (.id==$id) | [.protocol_groups | .[]] | @csv' | sed 's/"//g');IFS=","; for i in $PG;do tempPGName=$(cat $org.protocol_groups | jq -r --arg i "$i" .'[] | select (.id==$i) | .name'); proto+="$tempPGName "; done; source="";Find_Name_source; target=""; Find_Name_target; echo $id,$name,$created_at,$description,$enabled,$modified_at,$source,$target,$proto | sed 's/\\//g' | sed 's/"//g' >> $fileName.csv; done;


fi

if [ "$menu" == "100" ] || [ "$menu" == "7" ]; then
#Egress
echo "" >> $fileName.csv
echo "" >> $fileName.csv
echo "" >> $fileName.csv
echo "Writing Egress rules"
echo "Egress" >> $fileName.csv
echo "ID,Name,Source,Target,Via" >> $fileName.csv
cat $org.Egress | jq .'[] | [.id, .name, .via] | @csv' | sed 's/\\//g' | sed 's/"//g' | while IFS=$"," read -r id name via;do sources=$(cat $org.Egress | jq --arg id "$id" .'[] | select (.id==$id) | [.sources | .[]] | @csv' | sed 's/\\//g' | sed 's/"//g' | sed 's/,/ /g');destinations=$(cat $org.Egress | jq --arg id "$id" .'[] | select (.id==$id) | [.destinations | .[]] | @csv' | sed 's/\\//g' | sed 's/"//g' | sed 's/,/ /g');via=$(echo $via | sed 's/"//g'); echo $id,$name,$sources,$destinations,$via >> $fileName.csv; done;
fi

if [ "$menu" == "100" ] || [ "$menu" == "8" ]; then
#routing groups
echo "" >> $fileName.csv
echo "" >> $fileName.csv
echo "" >> $fileName.csv
echo "Routing Groups" >> $fileName.csv
echo ID,Name,Mapped elements,Sources >> $fileName.csv
echo "writing Routing Groups"
cat $org.routing_groups | jq .'[] | [.name, .id] | @csv' | sed 's/\\//g' | while IFS=$',' read -r name id; do id=$(echo $id | sed 's/\\r//g' | sed 's/"//g'); me=$(cat $org.routing_groups | jq --arg id "$id" .'[] | select (.id==$id) | [(.mapped_elements_ids | .[])] | @csv' | sed 's/\\//g' | sed 's/,//g' | sed 's/"//g'); s=$(cat $org.routing_groups | jq --arg id "$id" .'[] | select (.id==$id) | [(.sources | .[])] | @csv' | sed 's/\\//g' | sed 's/,//g' | sed 's/"//g');id=$(echo $id | sed 's/"//g'); echo $id,$name,$me,$s, | sed 's/"//g' >> $fileName.csv ;done

fi

if [ "$menu" == "100" ] || [ "$menu" == "9" ]; then
#EasyLinks
echo "" >> $fileName.csv
echo "" >> $fileName.csv
echo "" >> $fileName.csv
echo "EasyLinks" >> $fileName.csv
echo "ID,Name,Mapped elements,Domain name,IP/HostName (null=probably it's subnet),Port,Protocol,viewers" >> $fileName.csv
echo "writing EasyLinks"
cat $org.EasyLinks | jq .'[] | [.name, .id, .mapped_element_id, .domain_name, .port, .protocol] | @csv' | while IFS=$',' read -r name id mapped_element domain_name port protocol; do mapped_element=$(echo $mapped_element | sed 's/"//g' | sed 's/\\//g'); id=$(echo $id | sed 's/\\"//g'); protocol=$(echo $protocol | sed 's/"//'); viewers=$(cat $org.EasyLinks | jq --arg id "$id" .'[] | select (.id==$id) | [(.viewers | .[] )]| @csv' | sed 's/\\//g' | sed 's/,//g' | sed 's/"/ /g'); IP=$(cat $org.Network_Elements | jq --arg mapped_element "$mapped_element" .'[] | select (.id==$mapped_element) | .mapped_service' | sed 's/"//g'); echo $id,$name,$mapped_element,$domain_name,$IP,$port,$protocol,$viewers | sed 's/\\//g' | sed 's/"//g' >> $fileName.csv ;done

fi

if [ "$menu" == "100" ] || [ "$menu" == "10" ]; then
#Split tunnel
echo "Checking Split-tunnel configuration"
echo "" >> $fileName.csv
echo "" >> $fileName.csv
echo "" >> $fileName.csv
echo "Split Tunnel" >> $fileName.csv
echo "ID,Name,All org,Members" >> $fileName.csv

cat $org.Device_Settings | jq .'[] | select (.split_tunnel==true) | [.name, .id, .apply_on_org] | @csv' | while IFS=$',' read -r name id apply_on_org; do id=$(echo $id | sed 's/\\"//g' | sed 's/"//g' ); members=$(cat $org.Device_Settings | jq --arg id "$id" .'[] | select (.id==$id) | [.apply_to_entities | .[]] | @csv' | sed 's/\\//g' | sed 's/"//g' | sed 's/,/ /g'); echo $id,$name,$apply_on_org,$members | sed 's/\\//g' | sed 's/"//g' >> $fileName.csv;done;
fi

if [ "$menu" == "100" ] || [ "$menu" == "11" ]; then
#IDP's
echo "" >> $fileName.csv
echo "" >> $fileName.csv
echo "" >> $fileName.csv
echo "IDP's" >> $fileName.csv
echo "ID,Name,Created at,Modified at,SAML,SCIM key (if defined)" >> $fileName.csv

echo "writing IDP's"
cat idps.$org.csv | jq .'[] | [.id, .name, .created_at, .modified_at,(.saml_config | .certificate), (.scim_config | .api_key_id)] | @csv' | while IFS=$',' read -r id name created_at modified_at SAML SCIM; do if grep "BEGIN CERTIFICATE" <<< "$SAML" &> /dev/null; then SAML=true; else SAML=false;fi; echo $id,$name,$created_at,$modified_at,$SAML,$SCIM | sed 's/\\//g' | sed 's/"/ /g' >> $fileName.csv; done;
fi

if [ "$menu" == "100" ] || [ "$menu" == "12" ]; then
#Log Streaming
echo "Checking Log Streaming configuration"
echo "" >> $fileName.csv
echo "" >> $fileName.csv
echo "" >> $fileName.csv
echo "Log Streaming" >> $fileName.csv
echo "ID,Name,SIEM Configuration (URL:Port:Protocol)" >> $fileName.csv

cat $org.Access.Bridge | jq .'[] | select (.type=="siem") | [.name, .id] | @csv' | while IFS=$',' read -r name id; do id=$(echo $id | sed 's/\\"//g' | sed 's/"//g' );
Siem_Configuration=$(cat $org.Access.Bridge | jq --arg id "$id" .'[] | select (.id==$id) | .siem_config | [.endpoints | .[] | .[]]| @csv' | sed 's/\\//g' | sed 's/"//g' | sed '
s/,/:/g'); echo $id,$name,$Siem_Configuration | sed 's/\\//g' | sed 's/"//g' >> $fileName.csv ;done;
fi

rm idps.$org.csv $org.routing_groups $org.EasyLinks $org.Network_Elements $org.Device_Settings $org.MP $org.Access.Bridge $org.policies $org.groups $org.protocol_groups $org.roles $org.users $org.active.users &> /dev/null
echo "the requested data exported to $fileName.csv"
