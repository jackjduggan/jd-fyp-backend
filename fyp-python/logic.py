import subprocess, os

"""
The purpose of this script is to direct the pipeline depending
upon the request details
"""

def execute_terraform_script(provider, hostname, operating_system, cpu_cores):

    provider = provider.lower() # ensure it's lower-case

    # Determine which terraform directory, based on provider
    script_path = f"fyp-terraform-{provider}/run-terraform-{provider}.sh" 

    print(f"Preparing to execute Terraform script for {provider.upper()} provider...")

    # Check if the script exists
    if not os.path.exists(script_path):
        print(f"Error: Terraform script not found at {script_path}. Please ensure it exists and try again.")
        return
        
    print(f"Executing: {script_path} with parameters hostname={hostname}, operating_system={operating_system}, cpu_cores={cpu_cores}")

    # Execute the bash script with parameters
    try:
        subprocess.run(["sh", script_path, hostname, operating_system, cpu_cores], check=True)
        print("Terraform script executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to execute Terraform script: {e}")
        return

# Example call
execute_terraform_script("aws", "example-hostname", "Ubuntu", "2")



