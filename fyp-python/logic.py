import subprocess, os, json
import asyncio, websockets

"""
The purpose of this script is to direct the pipeline depending
upon the request details
"""

def execute_terraform_script(provider, hostname, operating_system, cpu_cores, unique_filename, callback):

    provider = provider.lower() # ensure it's lower-case
    original_dir = os.getcwd()

    # Determine which terraform directory, based on provider
    terraform_dir = f"fyp-terraform-{provider}"
    script_path = f"run-terraform-{provider}.sh" # relative path

    print(f"Preparing to execute Terraform script for {provider.upper()} provider...")

    # Check if the terraform directory exists
    if not os.path.exists(terraform_dir):
        print(f"Error: Terraform directory not found at {terraform_dir}. Please ensure it exists and try again.")
        return

    # Change to the terraform directory
    os.chdir(terraform_dir)
    print(f"Changed directory to {terraform_dir}/")

    # Check if the script exists in the current directory
    if not os.path.exists(script_path):
        print(f"Error: Terraform script not found at {script_path}. Please ensure it exists and try again.")
        # Change back to the original directory before returning
        os.chdir(original_dir)
        return

    print(f"Executing: {script_path} with parameters hostname={hostname}, operating_system={operating_system}, cpu_cores={cpu_cores}")

    # Execute the bash script with parameters
    try:
        subprocess.run(["sh", script_path, hostname, operating_system, cpu_cores], check=True)
        print("Terraform script executed successfully.")

        # Fetch output for IP address
        result = subprocess.run(["terraform", "output", "--raw", "instance_ip"], capture_output=True, text=True)
        ip_address = result.stdout.strip()
        print(f"Provisioned IP address: {ip_address}")


        try:
            with open(unique_filename, 'r+') as file:
                data = json.load(file)
                data['server_ip'] = ip_address
                file.seek(0)
                json.dump(data, file, indent=4)
                file.truncate()

            # Call the callback to start the IP update process
            if callback:
                callback(unique_filename)

        except Exception as e:
            print(f"Failed to update JSON file with IP address: {e}")


        # Send IP address via WebSocket
        #asyncio.run(send_ip_via_websocket(websocket_uri, ip_address))

    except subprocess.CalledProcessError as e:
        print(f"Failed to execute Terraform script: {e}")

async def send_ip_via_websocket(uri, ip_address):
    async with websockets.connect(uri) as websocket:
        print("Attempting to send IP via WebSocket.")
        await websocket.send(json.dumps({'type': 'ip_address', 'ip': ip_address}))
        print("IP address sent via WebSocket.")

# Example call
#execute_terraform_script("aws", "testing-logic-provisoning", "ubuntu", "2")



