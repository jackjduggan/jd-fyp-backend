#!/bin/bash

# This script applies a Terraform configuration for AWS provider
# This script is called from fyp-python/logic.py with arguments

HOSTNAME=$1
OPERATING_SYSTEM=$2
CPU_CORES=$3

#if [$OPERATING_SYSTEM == "ubuntu"]; then
    # OPERATING_SYSTEM=[ami-xxxxxxx]

#if [$CPU_CORES == "1"]; then
# CPU_CORES=[t2-nano]

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
# expected_terraform_dir="fyp-terraform-aws/"

# # Check if the script is not executed from the expected Terraform directory
# if [ "$(pwd)" != "${expected_terraform_dir}" ]; then
#     echo "Error: Please run the script from the Terraform directory (${expected_terraform_dir})."
#     exit 1
# fi

# Initialize Terraform
echo "Initializing Terraform in directory $expected_terraform_dir..."
terraform init

# Apply the Terraform configuration, passing the hostname as a variable
echo "Applying Terraform with details: $HOSTNAME, $OPERATING_SYSTEM, $CPU_CORES..."
terraform apply --auto-approve \
                -var="hostname=$HOSTNAME" \
                -var="operating_system"=$OPERATING_SYSTEM \
                -var="cpu_cores"=$CPU_CORES
echo "Script working.. futher functionality WIP. Press CRTL+C to end."