# Meta Networks Scripts Page

*The following scripts will provide the option to import\export data from your proofpoint | meta networks tenant*

## Before you begin

Verify that you have the following:
1. jq - Json processor [download now]
2. Proofpoint Meta account with an administrator account

Follow these steps to use the Proofpoint Meta API script for data export:
* Generate an API key and API ID.
* Create a file with the generated API secret.
* Create a file with the generated API ID.
* If using Managed Security Service Provider (MSSP) mode, create a file with the required organization name.
> **Note:** The files can be saved in a TXT or CSV formats, the script will process only the first line of the file to looking for the required data.

## Editing the script

1. Open the script file.
2. Edit the path for the ```API_KEY, API_ID``` and for ```SUB_ORG``` (if exists) in lines 3 to 7 and paste the path to the previously-created files.<br/>
See the script sample below:
```bash
#Please fill the path to the API before running the script (only csv or txt file)
API_KEY="Path/to/the/API/Key/file"
API_ID="Path/to/the/API/ID/file"
#Sub_Org is Optional, not optional for MSSP
Sub_ORG="Path/to/the/Sub/ORG/file"
```

## Scripts Libary
### bash
- ```export_data_to_csv```:<br/>
this script providing the option to export the following data:<br/>
  1. Active users last 30 days - Minimum,Average,Maximum<br/>
  2. Roles - ID,Name,Role<br/>
  3. MetaPorts - ID,Name,Enabled,Mapped Elements<br/>
  4. Mapped Subnets - ID,Name,CIDR,DNS Suffix:Enterprise DNS (true\flase),Host Name<br/>
  5. Mapped service - ID,Name,IP\HostName,DNS Suffix<br/>
  6. Policies - ID,Name,Created at,Description,Enabled,Modified at,Sources,Target,Protocols<br/>
  7. Egress ID,Name,Source,Target,Via<br/>
  8. Routing Groups - ID,Name,Mapped elements,Sources<br/>
  9. Easy Links - ID,Name,Mapped elements,Domain name,IP/HostName (null=probably it's subnet),Port,Protocol,Viewers<br/>
  10. Split Tunnel Configuration - ID,Name,All org,Members<br/>
  11. IDPS - ID,Name,Created at,Modified at,SAML,SCIM key (if defined)<br/>
  12. Log Streaming - ID,Name,SIEM Configuration (URL:Port:Protocol)<br/>
  13. All data above<br/>


- ```create_multiple_mappedservices_from_csv.sh:```<br/>
This script will provide the option to import multiple mapped services that has been writen in a csv file<br/>
the csv file format should be as following: name,description,ip\hostname,aliase,MetaPort-ID

- ```get_devices_version_to.csv.sh```:<br/>
this script will provide a csv file with the devices and the related agent version<br/>
the CSV format will present as the following: created_at,id,name,owner_id,platform_version,platform,serial_number<br/>

- ```get_enabled_users_and_groups_realation_.sh```:<br/>
this script will provide a csv file with all enabled users and the group\s they are part of.<br/>
the csv foramt will be as following: Email,Family Name, Private Name,Groups,Role<br/>

- ```pc_statistics_to_csv.sh```:<br/>
this script will provide the option to get statistics regarding failed posture check attempt<br/>

- ```users_throughput_to_csv.sh```:<br/>
This script will provide the option to recieve a csv file with the 100 top users by throughput for organization<br/>

### powershell
- ```enable_ipv6_windows.ps1```:<br/>
this script will provide the option to enable ipv6 on windows client, UAC will pop up if the script isn't runing with admin permissions<br/>

### python
- ```create_users_from_csv.py```:<br/>
This script will provide the option to create multiple users that has been writen in a csv file

- ```enable_metaconnect_all.py```: <br/>
This script will provide the option to enable to enable mc for all users in org 

- ```create_routing_group.py```: <br/>
This script creates a single user routing group containing the group "All Users" as source

- ```egress_rule.py```: <br/>
This script creates Egress PoP Exception rules for several Microsoft Services.

- ```egressdestination.py```: <br/>
this script will provide the ability to patch multiple destinations to existing egress rule from file

- ```enable_audit_settings.py```: <br/>
This script enables audit settings mode to log Internet traffic and enable Meta Connect logs for created users

- ```generate_fqdn.py```: <br/>
This script generates DNS record per device/client (aka device alias).
The DNS record is created from the device name and optionally concatenated
with a domain name

- ```macOS_pc_bestpractices.py```: <br/>
This script implements several macOS security posture checks best practices in audit (Log only mode)

- ```meta_device_mgmt.py```: <br/>
This script creates a customized device settings and user settings

- ```version_control.py```: <br/>
This script configure the version control feature profile.

- ```windows_pc_bestpractices.py```: <br/>
This script implements several Windows security posture checks best practices in audit (Log only mode)

- ```create_content_categories_from_file.py```: <br/>
This script will provide the ability to create "content categories" with a list of URL's or cntents categories

- ```unique_users_per_org.py```: <br/>
This script will provide the ability to get number of connected unique users per month.

## report a bug
for reporting a bug please contact your proofpoint sales engineer.<br/>

[download now]: https://stedolan.github.io/jq/download/

