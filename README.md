# Code assigment

Code assigment is a project that will have the capacity of
- Create a simple AWS infraestructure, with three ec2 instances and one security group, allowing these ec2 instances to connect through SSH
- Generate a report with some resource stadistics about:
    - Log the current running processes
    - Log top 3 applications that are consuming CPU and memory in each server
    - Log how much capacity is remaining on each server, expressed in several human-readable ways
    - All these information will be save in a log file, where the name will contain the server where it's extracting the information

## Prerequisites
- This project is design to run on Linux distributions
- Python3 version 3 must be installed as well as pip3
- Terraform must be installed and configure
- Have aws-cli installed and aws configured with secret keys that allows interaction with SSH between local and remote ec2 instances
- The user configure for aws access must have allow to check and make installation of packages in the remote server

## Setup environment
Folder ```infrastructure``` contains a terraform file, ```ec2-creation.tf```, that will create the basic aws infrastructure for this project:
- One security group that allows SSH connections to ec2 instances
- 3 ec2 instances what have as security group the previous one create and the tag ```codeassigment```

In this section you can configure the profile and access to aws, defining the provider and key access
```
provider "aws" {
  shared_credentials_file = "~/.aws/credentials"
  region                  = "us-east-1"
  profile                 = "default"
}
```
By default, it will connect with the ```default``` profile credentials for aws

In order to execute this file, navigate to ```infrastructure``` folder and execute:
```
terraform init 
terraform plan
terraform apply
```
Follow the standard procedure of terraform to create this infrastructure. It's imperative to run this file since the main workflow will search in aws ec2 inventory and return all instances that match with the tag ```codeassigment```. If doesn't exist ec2 with this tag, won't exist a list of servers to iterate.

## Usage
Clone this repository and execute the bash script as follow:

```
bash app_exec.sh USER /DESTINATION_FOLDER

where:
USER will be the user able to do ssh to aws ec2 instances and execute python commands remotely
DESTINATION_FOLDER will be the destination folder in the remote servers where 

Example: bash app_exec.sh ec2-user /tmp

```
Application will be located inside of ```source``` in ```DESTINATION_FOLDER``` folder. Once the script it's executed it will execute python script ```check_env.py``` that will check if all python3 libraries necessary for the application are installed. Then, it will search in aws ec2 list all instances that match with tag ```codeassigment``` and finally, iterate in each one of them and generate a report in path ```DESTINATION_FOLDER/source/log_files```

## Log files
Format of the log file generated in ```DESTINATION_FOLDER/source/log_files```

```assigment_log_TIMESTAMP_EXECUTION_MOMENT_IP_SERVER.txt

Example: assigment_log_2021-05-02-12:48:21.727724_ip-172-31-31-71.ec2.internal.txt

``` 
### Output example
```
>>>>>>>>>List of all process<<<<<<<<<<
PID       Name       Username      Creation datetime       CPU %     Memory %
1         systemd    root          05/02/2021, 00:00:00    0.00 %    0.54 %
.
.
.
List all current running process

>>>>>>>>>>List of top 3 memory usage process<<<<<<<<<<
 PID 	  Name		                Username		Creation datetime			CPU %			Memory %
40868	  Google Chrome	            a744885         04/30/2021, 00:00:00		0.00 %			3.59 %
66132	  Microsoft Outlook			a744885			04/26/2021, 00:00:00	    0.00 %			2.79 %
50009	  firefox				    a744885			04/23/2021, 00:00:00		0.00 %			2.22 %

>>>>>>>>>>List of top 3 CPU usage process<<<<<<<<<<
 PID 		        Name    		Username	    Creation datetime			         CPU %			Memory %
108			loginwindow				root			04/19/2021, 00:00:00				0.00 %			0.34 %
416			coreauthd				a744885			04/19/2021, 00:00:00				0.00 %			0.06 %
418			cfprefsd				a744885			04/19/2021, 00:00:00				0.00 %			0.03 %

>>>>>>>>>>Disk information<<<<<<<<<<
=== Device: /dev/disk1s1 ===
  Mount point: /
  File system type: apfs
  Partition Mount options: rw,local,rootfs,dovolfs,journaled,multilabel
  Total Size: {'PB': '0.0', 'TB': '0.228', 'GB': '233.469', 'MB': '239072.395', 'KB': '244810132.0', 'bytes': '250685575168.0'}
  Used: {'PB': '0.0', 'TB': '0.117', 'GB': '119.993', 'MB': '122873.004', 'KB': '125821956.0', 'bytes': '128841682944.0'}
  Free: {'PB': '0.0', 'TB': '0.103', 'GB': '105.828', 'MB': '108367.969', 'KB': '110968800.0', 'bytes': '113632051200.0'}
  Percentage: 53.10%
```