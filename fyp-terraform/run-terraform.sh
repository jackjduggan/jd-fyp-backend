#!/bin/bash

# The hostname is passed as the first argument
hostname_value="$1"

if [ -z "$hostname_value" ]; then
    echo "Error: No hostname value provided."
    exit 1
fi

echo "Hostname value provided: $hostname_value"

# Initialize Terraform
echo "Initializing Terraform..."
#terraform init

# Apply the Terraform configuration, passing the hostname as a variable
echo "Applying Terraform with hostname: $hostname_value"
#terraform apply -var="hostname=$hostname_value" -auto-approve
echo "Script working.. futher functionality WIP. Press CRTL+C to end."