from flask import Flask, request
from flask_cors import CORS
import json
import uuid
import os
import subprocess
import time
from flask_socketio import SocketIO
from send import send_email
from threading import Thread
from queue import Queue
from logic import execute_terraform_script
from secret.config import SENDER_EMAIL, SENDER_PASSWORD, RECEIVER_EMAIL
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
socketio = SocketIO(app, cors_allowed_origins="*")

current_dir = "/home/jack/Code/fyp-backend" # local vm

### -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# FORM HANDLE & APPROVAL FUNCTION
###

@app.route('/submit', methods=['POST'])
def handle_form():

    ### --------------------------------------------------------------------
    # FORM HANDLING
    ###

    data = request.json
    print("Received data:", data)

    # Generate a unique filename and ensure the vars/ directory exists
    unique_id = uuid.uuid4()
    unique_filename = f"fyp-python/vars/data_{unique_id}.json"
    print(f"Generated unique filename: {unique_filename}")

    # Add unique id to the data
    data['uid'] = str(unique_id)

    # Ensure directory exists
    try:
        os.makedirs(os.path.dirname(unique_filename), exist_ok=True)
        print(f"Ensured that directory {os.path.dirname(unique_filename)} exists.")
    except Exception as e:
        print(f"Error ensuring directory exists: {e}")
        return {"error": "Failed to ensure directory existence"}, 500

    # Save the received data to the file for logging
    try:
        with open(unique_filename, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"Successfully saved data to {unique_filename}")
    except Exception as e:
        print(f"Error saving data to file: {e}")
        return {"error": "Failed to save data to file"}, 500

    ### --------------------------------------------------------------------
    # APPROVAL SYSTEM
    ###

    # Format request details
    hostname = data.get('name', 'No name provided')
    provider = data.get('provider', 'No provider provided')
    operating_system = data.get('os', 'No OS provided')  # Be cautious with variable name 'os' as it's also a module name
    cpu_cores = data.get('cpu_cores', 'No CPU cores provided')

    request_details = f"""<br>
    <i>Hostname:</i> {hostname}<br>
    <i>Provider:</i> {provider}<br>
    <i>OS:</i> {operating_system}<br>
    <i>CPU Cores:</i> {cpu_cores}
    """

    time_requested = data.get('date')
    requester_email = data.get('email', 'No email provided')
    subject = "Approval Request | PLEASE REPLY"


    # Send the approval request email
    send_email(SENDER_EMAIL, SENDER_PASSWORD, RECEIVER_EMAIL, subject, request_details, time_requested, requester_email, str(unique_id))
    # Emit update to frontend
    socketio.emit('status_update', {'message': 'Your request has been forwarded for approval'})

    # Wait for approval for up to 5 minutes & execute read.py while loop.
    approval_status = "denied" # should default to denied
    start_time = time.time() # store start time as current time
    print(f"Started timer at {start_time}")
    while time.time() - start_time < 300: # 5 minutes
        try:
            # runs read.py in a loop until timer runs out or approval is received
            poll_approval = subprocess.run(['python3', 'fyp-python/read.py'], capture_output=True, text=True)
            print(poll_approval.stdout)
            print(f"Poll attempt executed. Time remaining {300-(time.time() - start_time)}")
            if "Approved" in poll_approval.stdout:
                approval_status = "approved"
                break
            time.sleep(10)
        except Exception as e:
            print(f"Error during approval check: {e}")
            break
    
    # Update data with approval status and save to file
    data['approval'] = approval_status
    try:
        with open(unique_filename, 'w') as file:
            json.dump(data, file, indent=4)
        print(f"Data updated with approval status: {approval_status}")
        socketio.emit('status_update', {'message': 'Approval received. Initializing provisioning.'})
    except Exception as e:
        print(f"Error updating data file with approval status: {e}")
        return {"error": "Failed to update data with approval status"}, 500

    ### --------------------------------------------------------------------
    # EXECUTE SCRIPT
    ###
    if approval_status == "approved":  # proceed only if approved
        try:
            print("Approval received. Attempting to execute the bash script with provided data...")
            provider = data.get('provider', 'aws')  # Defaulting to AWS
            hostname = data.get('name', 'No name provided')
            operating_system = data.get('os', 'No OS provided')
            cpu_cores = data.get('cpu_cores', '1')
            absolute_unique_filename = os.path.abspath(unique_filename)

            execute_terraform_script(provider, hostname, operating_system, cpu_cores, absolute_unique_filename)
            
        except Exception as e:
            print(f"Error executing Terraform provisioning script: {e}")
            return {"error": "Failed to execute the Terraform provisioning script"}, 500

    return {"message": "Data saved and script executed successfully"}, 200

### -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# SERVER EXECUTION
###

if __name__ == '__main__':
    #app.run(debug=True, host='0.0.0.0', port=5000)
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)   
