#!/bin/bash

##################################
# BASE SCRIPT APPLICATION
# DESCRIPTION
# it will get all instances previous created with terraform
# with tag "codeassigment" and then, check if python libraries are installed in each server.
# If requirements are complete, execute the report
####################################

# Get username and base path default for application that came as parameter
username="$1"
base_default_path="$2"

# MAIN WORKFLOW
# 1- Obtain all ip address previously created with terraform
ip_server_address=$(aws ec2 describe-instances --profile="codeassigment" \
  --filter "Name=tag-value,Values=codeassigment" \
  --query "Reservations[*].Instances[*].[PublicDnsName]" \
  --output text)

# 2- Iterate each one of them and copy the code to generate report
for server in $(echo "${ip_server_address}" | tr ";" "\n")
do
  echo ">>>>>>>>>>"
  echo "Copy core application in path ${base_default_path} on server ${server} ... "
  scp -r source/ "${username}"@"${server}":"${base_default_path}"
  echo ">>>>>>>>>>"
done

# 3- Iterate each one of them and check python libraries requirements for the application
for server in $(echo "${ip_server_address}" | tr ";" "\n")
do
  echo ">>>>>>>>>>"
  echo "Checking requirement python3 libraries on server ${server}."
  ssh "${username}"@"${server}" "python3 ${base_default_path}/source/check_env.py"
  echo ">>>>>>>>>>"
done

# 4- Iterate each one of them and execute the application
for server in $(echo "${ip_server_address}" | tr ";" "\n")
do
  echo ">>>>>>>>>>"
  echo "Executing report on server ${server}. Report will be in ${server} on path ${base_default_path}/source/log_files"
  ssh "${username}"@"${server}" "python3 ${base_default_path}/source/__main__.py ${base_default_path}/source"
  echo ">>>>>>>>>>"
done