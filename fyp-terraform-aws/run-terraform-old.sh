#!/bin/bash

# This script applies a Terraform configuration for AWS provider
# This script is called from fyp-python/logic.py with arguments

HOSTNAME=$1
OPERATING_SYSTEM=$2
CPU_CORES=$3

echo "Running Terraform for AWS with the following parameters:"
echo "Hostname: $HOSTNAME"
echo "Operating System: $OPERATING_SYSTEM"
echo "CPU Cores: $CPU_CORES"

# Check AWS credentials
# Code taken from previous assignment https://github.com/jackjduggan/cc2-terraform-ansible/blob/main/main.sh
s3_output=$(aws s3 ls 2>&1)

if echo "$s3_output" | grep -q "An error occurred"; then
    echo "Error with AWS credentials: $s3_output"
    echo "Please check your credentials are configured and valid."
    exit 1
fi

echo "AWS credentials are valid... Proceeding"

# Set the expected Terraform directory
expected_terraform_dir="fyp-terraform-aws/"

# Check if the script is not executed from the expected Terraform directory
if [ "$(pwd)" != "${expected_terraform_dir}" ]; then
    echo "Error: Please run the script from the Terraform directory (${expected_terraform_dir})."
    exit 1
fi

# Path to the JSON file
#json_file="/home/jackd/Code/fyp-skeleton/fyp-python/vars/prov-req*.json"

# Retrieve the hostname value passed as an argument
hostname_value="$1"
# Check if hostname value exists
if [ -z "$hostname_value" ]; then
    echo "Error: No hostname value provided."
    exit 1
fi

# DynamoDB table name and the primary key of the item
table_name="InProv_Details_Table"
#primary_key="hostname"

# Use AWS CLI to get the item from DynamoDB
echo "Running command: aws dynamodb get-item --table-name \"$table_name\" --key \"{\\\"hostname\\\": {\\\"S\\\": \\\"$hostname_value\\\"}}\" --query \"Item.hostname.S\" --output text"
data=$(aws dynamodb get-item --table-name "$table_name" --key "{\"hostname\": {\"S\": \"$hostname_value\"}}" --query "Item.hostname.S" --output text)

# Check if the JSON file exists
# if [ -f $json_file ]; then
#     # Extract the hostname value from the JSON file
#     hostname_value=$(jq -r '.hostname' $json_file)

#     # Initialize Terraform
#     terraform init

#     # Apply the Terraform configuration with the hostname variable
#     terraform apply -var="hostname=$hostname_value" -auto-approve

# else
#     # If the "hostname.txt" file does not exist, display an error message
#     echo "Error: Variable file does not exist."
# fi

echo "Hostname value provided: $hostname_value"
echo "Data retrieved from DynamoDB: $data"

if [ "$data" ]; then
    hostname_only=$data
    # Check if hostname only has a value
    if [ -z "$hostname_only" ]; then
    echo "Error: Hostname value retrieved from DynamoDB is empty."
    exit 1
    fi

    # Initialize Terraform
    terraform init

    # Apply the Terraform configuration with the hostname variable
    terraform apply -var="hostname=$hostname_only" -auto-approve
else
    # If data is not retrieved, display an error message
    echo "Error: Unable to retrieve variable from DynamoDB."
    exit 1
fi