import imaplib
import email
from email.policy import default
import os
from secret.config import SENDER_EMAIL, SENDER_PASSWORD, RECEIVER_EMAIL

# Enable debugging for IMAP commands
#imaplib.Debug = 4

# Connect to the IMAP server and log in
m = imaplib.IMAP4_SSL("imap.gmail.com", 993)
m.login(SENDER_EMAIL, SENDER_PASSWORD)
m.select('inbox')  # Select the inbox

# Define the function to check if a UID has been processed
def is_uid_processed(uid):
    if not os.path.exists("fyp-python/db/processed_uids.txt"):
        return False
    with open("fyp-python/db/processed_uids.txt", "r") as file:
        processed_uids = file.read().splitlines()
    return uid in processed_uids

# Define the function to store processed UIDs
def store_processed_uid(uid):
    with open("fyp-python/db/processed_uids.txt", "a") as file:
        file.write(f"{uid}\n")

# Search for emails from the specified sender
query = f'(FROM "{RECEIVER_EMAIL}")'
result, data = m.uid('search', None, query)
print(f"Search result: {result}, Data: {data}")

if result == 'OK':
    for num in data[0].split():
        uid = num.decode('utf-8')
        if is_uid_processed(uid):
            print(f"Email UID {uid} already processed, skipping.")
            continue  # Skip if already processed

        # Fetch the email by UID
        result, data = m.uid('fetch', uid, '(RFC822)')
        print(f"Fetch result: {result}, Data: {data}")
        if result == "OK" and data[0] is not None:
            # Parse the email content
            raw_email = data[0][1]
            email_message = email.message_from_bytes(raw_email, policy=default)

            # Check if the email is multipart
            if email_message.is_multipart():
                for part in email_message.walk():
                    # Only process text/plain parts
                    if part.get_content_type() == "text/plain":
                        body = part.get_payload(decode=True).decode("utf-8")
                        if "approve" in body.lower():
                            print("Approved")
                            store_processed_uid(uid)
                            break  # Stop checking other parts
                        else:
                            print("Denied")
            else:
                # Process non-multipart emails
                body = email_message.get_payload(decode=True).decode("utf-8")
                if "approve" in body.lower():
                    print("Approved")
                    store_processed_uid(uid)
                else:
                    print("Denied")
        else:
            print(f"Failed to fetch or no data for UID {uid}")

# Logout from the server
m.close()
m.logout()


# Inspired by below article, adapted for my needs.
# ref: https://alluaravind1313.medium.com/email-reading-using-python-imaplib-2d50912c119